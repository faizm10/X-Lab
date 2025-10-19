"""
IBM Careers Scraper - General Approach
Scrapes job listings from IBM's career page with multiple search strategies
"""
import asyncio
from typing import List, Dict, Optional
import httpx
from bs4 import BeautifulSoup
import logging
import re
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class IBMGeneralScraper:
    """General IBM scraper that tries multiple search strategies"""
    
    COMPANY_NAME = "IBM"
    
    def __init__(self):
        """Initialize the IBM scraper"""
        pass
        
    async def scrape(self) -> List[Dict[str, str]]:
        """
        Scrape job postings from IBM careers page using multiple strategies
        
        Returns:
            List of job dictionaries
        """
        all_jobs = []
        
        try:
            async with httpx.AsyncClient(
                timeout=30.0,
                follow_redirects=True,
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                }
            ) as client:
                
                # Strategy 1: Search for Software Engineering jobs in Canada
                jobs1 = await self._scrape_strategy_1(client)
                all_jobs.extend(jobs1)
                
                # Strategy 2: Search for Internship jobs
                jobs2 = await self._scrape_strategy_2(client)
                all_jobs.extend(jobs2)
                
                # Strategy 3: Search for general Software jobs
                jobs3 = await self._scrape_strategy_3(client)
                all_jobs.extend(jobs3)
                
        except Exception as e:
            logger.error(f"Error scraping IBM: {e}")
            raise
        
        # Remove duplicates based on URL
        unique_jobs = []
        seen_urls = set()
        for job in all_jobs:
            if job['url'] not in seen_urls:
                unique_jobs.append(job)
                seen_urls.add(job['url'])
        
        logger.info(f"Total unique IBM jobs found: {len(unique_jobs)}")
        return unique_jobs
    
    async def _scrape_strategy_1(self, client: httpx.AsyncClient) -> List[Dict[str, str]]:
        """Strategy 1: Software Engineering + Internship + Canada"""
        try:
            url = "https://www.ibm.com/au-en/careers/search?field_keyword_08[0]=Software%20Engineering&field_keyword_18[0]=Internship&field_keyword_05[0]=Canada"
            logger.info(f"Strategy 1: Scraping {url}")
            
            response = await client.get(url)
            response.raise_for_status()
            
            return await self._extract_jobs_from_response(response)
            
        except Exception as e:
            logger.warning(f"Strategy 1 failed: {e}")
            return []
    
    async def _scrape_strategy_2(self, client: httpx.AsyncClient) -> List[Dict[str, str]]:
        """Strategy 2: Just Internship jobs"""
        try:
            url = "https://www.ibm.com/au-en/careers/search?field_keyword_18[0]=Internship"
            logger.info(f"Strategy 2: Scraping {url}")
            
            response = await client.get(url)
            response.raise_for_status()
            
            jobs = await self._extract_jobs_from_response(response)
            
            # Filter for software engineering related jobs
            filtered_jobs = []
            for job in jobs:
                title_lower = job['title'].lower()
                if any(keyword in title_lower for keyword in ['software', 'engineer', 'developer', 'intern']):
                    filtered_jobs.append(job)
            
            return filtered_jobs
            
        except Exception as e:
            logger.warning(f"Strategy 2 failed: {e}")
            return []
    
    async def _scrape_strategy_3(self, client: httpx.AsyncClient) -> List[Dict[str, str]]:
        """Strategy 3: Software Engineering jobs in general"""
        try:
            url = "https://www.ibm.com/au-en/careers/search?field_keyword_08[0]=Software%20Engineering"
            logger.info(f"Strategy 3: Scraping {url}")
            
            response = await client.get(url)
            response.raise_for_status()
            
            jobs = await self._extract_jobs_from_response(response)
            
            # Filter for internship/entry level jobs
            filtered_jobs = []
            for job in jobs:
                title_lower = job['title'].lower()
                if any(keyword in title_lower for keyword in ['intern', 'co-op', 'entry', 'graduate', 'student']):
                    filtered_jobs.append(job)
            
            return filtered_jobs
            
        except Exception as e:
            logger.warning(f"Strategy 3 failed: {e}")
            return []
    
    async def _extract_jobs_from_response(self, response: httpx.Response) -> List[Dict[str, str]]:
        """Extract jobs from HTTP response"""
        jobs = []
        
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Log page info for debugging
            page_title = soup.find('title')
            if page_title:
                logger.debug(f"Page title: {page_title.get_text()}")
            
            # Try multiple extraction methods
            jobs.extend(self._extract_jobs_from_links(soup))
            jobs.extend(self._extract_jobs_from_structured_data(soup))
            
        except Exception as e:
            logger.warning(f"Error extracting jobs from response: {e}")
        
        return jobs
    
    def _extract_jobs_from_links(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract jobs by analyzing links"""
        jobs = []
        
        try:
            # Find all links that might be job postings
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                
                # Check if this looks like a job link
                if (('/careers/' in href or '/jobs/' in href or 'careers.ibm.com' in href) and 
                    text and len(text) > 5 and len(text) < 100 and
                    not any(skip in text.lower() for skip in ['login', 'register', 'sign in', 'home', 'about'])):
                    
                    # Make URL absolute
                    if href.startswith('/'):
                        href = f"https://www.ibm.com{href}"
                    elif not href.startswith('http'):
                        href = f"https://www.ibm.com/careers/{href}"
                    
                    # Create job ID
                    job_id = str(hash(href))[-8:]
                    unique_id = f"ibm_{job_id}"
                    
                    # Determine location and team from context
                    location = self._extract_location_from_context(link)
                    team = self._extract_team_from_title(text)
                    
                    job = {
                        "id": unique_id,
                        "company": self.COMPANY_NAME,
                        "title": text,
                        "team": team,
                        "location": location,
                        "url": href,
                        "description": None,
                        "posted_date": None
                    }
                    
                    jobs.append(job)
                    logger.debug(f"Found job: {text}")
            
        except Exception as e:
            logger.debug(f"Error extracting jobs from links: {e}")
        
        return jobs
    
    def _extract_jobs_from_structured_data(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract jobs from structured data (JSON-LD, etc.)"""
        jobs = []
        
        try:
            # Look for JSON-LD structured data
            scripts = soup.find_all('script', type='application/ld+json')
            
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    if isinstance(data, dict) and data.get('@type') == 'JobPosting':
                        job = self._parse_job_from_structured_data(data)
                        if job:
                            jobs.append(job)
                except (json.JSONDecodeError, ValueError):
                    continue
            
        except Exception as e:
            logger.debug(f"Error extracting jobs from structured data: {e}")
        
        return jobs
    
    def _parse_job_from_structured_data(self, data: dict) -> Optional[Dict[str, str]]:
        """Parse a job from structured data"""
        try:
            title = data.get('title', 'Unknown Title')
            url = data.get('url', '')
            
            if not url:
                return None
            
            # Make URL absolute
            if url.startswith('/'):
                url = f"https://www.ibm.com{url}"
            
            job_id = str(hash(url))[-8:]
            unique_id = f"ibm_{job_id}"
            
            return {
                "id": unique_id,
                "company": self.COMPANY_NAME,
                "title": title,
                "team": "Software Engineering",
                "location": "Canada",
                "url": url,
                "description": None,
                "posted_date": None
            }
            
        except Exception as e:
            logger.debug(f"Error parsing job from structured data: {e}")
            return None
    
    def _extract_location_from_context(self, element) -> str:
        """Extract location from element context"""
        try:
            # Look in parent elements for location info
            parent = element.parent
            for _ in range(3):  # Check up to 3 levels up
                if parent:
                    text = parent.get_text()
                    if any(city in text for city in ['Toronto', 'Vancouver', 'Montreal', 'Ottawa', 'Calgary']):
                        return 'Canada'
                    parent = parent.parent
                else:
                    break
        except:
            pass
        
        return 'Canada'  # Default
    
    def _extract_team_from_title(self, title: str) -> str:
        """Extract team/department from job title"""
        title_lower = title.lower()
        
        if 'software' in title_lower or 'engineer' in title_lower:
            return 'Software Engineering'
        elif 'data' in title_lower:
            return 'Data Science'
        elif 'ai' in title_lower or 'machine learning' in title_lower:
            return 'AI/ML'
        else:
            return 'Engineering'


# Convenience function for the scheduler
async def scrape_ibm_general() -> List[Dict[str, str]]:
    """
    Convenience function to scrape IBM jobs using general approach
    
    Returns:
        List of job dictionaries
    """
    scraper = IBMGeneralScraper()
    return await scraper.scrape()

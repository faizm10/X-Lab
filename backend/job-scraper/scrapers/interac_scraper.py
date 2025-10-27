"""
Interac Careers Scraper
Scrapes job listings from Interac's career page
"""
import asyncio
from typing import List, Dict, Optional
import httpx
import logging
from datetime import datetime
from bs4 import BeautifulSoup
import re
import json

logger = logging.getLogger(__name__)


class InteracScraper:
    """Scraper for Interac careers page"""
    
    BASE_URL = "https://www.interac.ca"
    SEARCH_URL = "https://www.interac.ca/en/careers"
    COMPANY_NAME = "Interac"
    
    def __init__(
        self, 
        keywords: Optional[List[str]] = None,
        location: Optional[str] = None,
        job_type: Optional[str] = None
    ):
        """
        Initialize the Interac scraper
        
        Args:
            keywords: List of keywords to search for (e.g., ["intern", "internship", "co-op"])
            location: Filter by location (e.g., "Toronto", "Vancouver")
            job_type: Filter by job type (e.g., "Internship", "Co-op")
        """
        self.keywords = keywords or ["intern", "internship", "co-op", "coop"]
        self.location = location
        self.job_type = job_type or "Internship"
        
    async def scrape(self) -> List[Dict[str, str]]:
        """
        Scrape all job postings from Interac careers page
        
        Returns:
            List of job dictionaries with keys: id, company, title, team, location, url
        """
        jobs = []
        
        try:
            async with httpx.AsyncClient(
                timeout=30.0,
                follow_redirects=True,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                }
            ) as client:
                logger.info(f"Scraping Interac careers: {self.SEARCH_URL}")
                
                response = await client.get(self.SEARCH_URL)
                response.raise_for_status()
                
                # Parse the HTML response
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract jobs from the page
                page_jobs = self._extract_jobs_from_html(soup)
                jobs.extend(page_jobs)
                logger.info(f"Scraped {len(page_jobs)} jobs from Interac")
                
        except Exception as e:
            logger.error(f"Error scraping Interac: {e}")
            raise
        
        logger.info(f"Total jobs scraped from Interac: {len(jobs)}")
        return jobs
    
    def _extract_jobs_from_html(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract all jobs from the HTML page"""
        jobs = []
        
        try:
            # Look for job listings - Interac might use different selectors
            job_selectors = [
                '.job-listing',
                '.career-item',
                '.job-item',
                '.position',
                '.job-card',
                '.career-card',
                'article',
                '.job',
                '[data-testid*="job"]',
                '[class*="job"]',
                '[class*="career"]',
                '[class*="position"]'
            ]
            
            job_elements = []
            for selector in job_selectors:
                elements = soup.select(selector)
                if elements:
                    job_elements = elements
                    logger.info(f"Found {len(elements)} job elements using selector: {selector}")
                    break
            
            if not job_elements:
                # Fallback: look for any div with job-related classes
                job_elements = soup.find_all('div', class_=re.compile(r'job|listing|career|position|card'))
                logger.info(f"Fallback: Found {len(job_elements)} potential job elements")
            
            for job_element in job_elements:
                try:
                    job_data = self._extract_job_data(job_element)
                    if job_data:
                        jobs.append(job_data)
                        logger.debug(f"Extracted job: {job_data.get('title', 'Unknown')}")
                except Exception as e:
                    logger.error(f"Error extracting job data: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")
        
        return jobs
    
    def _extract_job_data(self, job_element) -> Optional[Dict[str, str]]:
        """Extract job data from a single job element"""
        try:
            # Extract job title
            title = None
            title_selectors = [
                'h3 a',
                'h2 a',
                'h4 a',
                '.job-title a',
                '.title a',
                '.position-title a',
                'a[href*="/careers/"]',
                'a[href*="/jobs/"]',
                '.job-title',
                '.title',
                '.position-title',
                'h3',
                'h2',
                'h4'
            ]
            
            for selector in title_selectors:
                title_elem = job_element.select_one(selector)
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    break
            
            if not title:
                # Try to find any link that might be a job title
                links = job_element.find_all('a', href=True)
                for link in links:
                    if any(keyword in link.get('href', '').lower() for keyword in ['career', 'job', 'position']):
                        title = link.get_text(strip=True)
                        break
            
            if not title:
                logger.debug("No title found for job element")
                return None
            
            # Extract job URL
            url = None
            url_selectors = [
                'h3 a',
                'h2 a',
                'h4 a',
                '.job-title a',
                '.title a',
                '.position-title a',
                'a[href*="/careers/"]',
                'a[href*="/jobs/"]'
            ]
            
            for selector in url_selectors:
                url_elem = job_element.select_one(selector)
                if url_elem and url_elem.get('href'):
                    url = url_elem.get('href')
                    if url.startswith('/'):
                        url = self.BASE_URL + url
                    break
            
            if not url:
                logger.debug(f"No URL found for job: {title}")
                return None
            
            # Extract location
            location = None
            location_selectors = [
                '.location',
                '.job-location',
                '.city',
                '.job-city',
                '.position-location',
                '[class*="location"]',
                '[class*="city"]'
            ]
            
            for selector in location_selectors:
                loc_elem = job_element.select_one(selector)
                if loc_elem:
                    location = loc_elem.get_text(strip=True)
                    break
            
            # Extract team/department
            team = None
            team_selectors = [
                '.department',
                '.team',
                '.job-category',
                '.position-category',
                '[class*="department"]',
                '[class*="team"]',
                '[class*="category"]'
            ]
            
            for selector in team_selectors:
                team_elem = job_element.select_one(selector)
                if team_elem:
                    team = team_elem.get_text(strip=True)
                    break
            
            # Extract job ID from URL
            job_id = None
            if url:
                # Try to extract job ID from URL
                id_match = re.search(r'/careers/(\d+)', url) or re.search(r'/jobs/(\d+)', url)
                if id_match:
                    job_id = id_match.group(1)
                else:
                    # Use URL hash as ID
                    job_id = str(hash(url))[-8:]  # Last 8 characters of hash
            
            if not job_id:
                job_id = f"interac_{hash(url)}"
            
            # Create unique ID with company prefix
            unique_id = f"interac_{job_id}"
            
            # Check if this is an intern/co-op position
            title_lower = title.lower()
            is_intern = any(keyword in title_lower for keyword in self.keywords)
            
            if not is_intern:
                logger.debug(f"Job '{title}' doesn't match intern keywords, skipping")
                return None
            
            job = {
                "id": unique_id,
                "company": self.COMPANY_NAME,
                "title": title,
                "team": team,
                "location": location,
                "url": url,
                "description": None,  # Would need to fetch individual job page
                "posted_date": None  # Interac doesn't always show posting dates
            }
            
            return job
            
        except Exception as e:
            logger.error(f"Error extracting job data from element: {e}")
            return None


# Convenience function for the scheduler
async def scrape_interac(
    keywords: Optional[List[str]] = None,
    location: Optional[str] = None,
    job_type: Optional[str] = "Internship"
) -> List[Dict[str, str]]:
    """
    Convenience function to scrape Interac jobs
    
    Args:
        keywords: List of keywords to search for (default: ["intern", "internship", "co-op", "coop"])
        location: Filter by location (optional)
        job_type: Filter by job type (default: "Internship")
        
    Returns:
        List of job dictionaries
    """
    if keywords is None:
        keywords = ["intern", "internship", "co-op", "coop"]
    
    scraper = InteracScraper(
        keywords=keywords,
        location=location,
        job_type=job_type
    )
    return await scraper.scrape()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(scrape_interac())

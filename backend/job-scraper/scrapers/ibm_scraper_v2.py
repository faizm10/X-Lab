"""
IBM Careers Scraper v2
Scrapes job listings from IBM's career page with improved parsing
"""
import asyncio
from typing import List, Dict, Optional
import httpx
from bs4 import BeautifulSoup
import logging
import re
import json
from datetime import datetime
from urllib.parse import urljoin, urlparse, parse_qs

logger = logging.getLogger(__name__)


class IBMScraperV2:
    """Improved scraper for IBM careers page"""
    
    BASE_URL = "https://www.ibm.com/au-en/careers/search"
    COMPANY_NAME = "IBM"
    
    def __init__(self, 
                 keyword_08: Optional[str] = "Software Engineering",
                 keyword_18: Optional[str] = "Internship", 
                 keyword_05: Optional[str] = "Canada"):
        """
        Initialize the IBM scraper
        
        Args:
            keyword_08: Filter by job function (default: "Software Engineering")
            keyword_18: Filter by job type (default: "Internship")
            keyword_05: Filter by location (default: "Canada")
        """
        self.keyword_08 = keyword_08
        self.keyword_18 = keyword_18
        self.keyword_05 = keyword_05
        
    def _build_url(self) -> str:
        """Build the URL with filters"""
        params = []
        
        if self.keyword_08:
            params.append(f"field_keyword_08[0]={self.keyword_08.replace(' ', '%20')}")
        if self.keyword_18:
            params.append(f"field_keyword_18[0]={self.keyword_18.replace(' ', '%20')}")
        if self.keyword_05:
            params.append(f"field_keyword_05[0]={self.keyword_05.replace(' ', '%20')}")
        
        url = f"{self.BASE_URL}?"
        if params:
            url += "&".join(params)
        
        return url
    
    async def scrape(self) -> List[Dict[str, str]]:
        """
        Scrape job postings from IBM careers page
        
        Returns:
            List of job dictionaries
        """
        jobs = []
        
        try:
            async with httpx.AsyncClient(
                timeout=30.0,
                follow_redirects=True,
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                }
            ) as client:
                url = self._build_url()
                logger.info(f"Scraping IBM careers page: {url}")
                
                response = await client.get(url)
                response.raise_for_status()
                
                logger.debug(f"Response status: {response.status_code}")
                logger.debug(f"Response length: {len(response.text)} characters")
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Log page title for debugging
                page_title = soup.find('title')
                if page_title:
                    logger.debug(f"Page title: {page_title.get_text()}")
                
                # Try to find job listings using multiple approaches
                jobs = await self._extract_jobs_multiple_approaches(soup, client)
                
        except Exception as e:
            logger.error(f"Error scraping IBM: {e}")
            raise
        
        logger.info(f"Total jobs scraped from IBM: {len(jobs)}")
        return jobs
    
    async def _extract_jobs_multiple_approaches(self, soup: BeautifulSoup, client: httpx.AsyncClient) -> List[Dict[str, str]]:
        """Try multiple approaches to extract jobs"""
        jobs = []
        
        # Approach 1: Look for JSON data in script tags
        jobs_from_json = self._extract_jobs_from_json(soup)
        if jobs_from_json:
            logger.info(f"Found {len(jobs_from_json)} jobs from JSON data")
            jobs.extend(jobs_from_json)
        
        # Approach 2: Look for standard HTML job listings
        jobs_from_html = self._extract_jobs_from_html(soup)
        if jobs_from_html:
            logger.info(f"Found {len(jobs_from_html)} jobs from HTML parsing")
            jobs.extend(jobs_from_html)
        
        # Approach 3: Look for any links that might be jobs
        jobs_from_links = self._extract_jobs_from_links(soup)
        if jobs_from_links:
            logger.info(f"Found {len(jobs_from_links)} jobs from link analysis")
            jobs.extend(jobs_from_links)
        
        # Remove duplicates based on URL
        unique_jobs = []
        seen_urls = set()
        for job in jobs:
            if job['url'] not in seen_urls:
                unique_jobs.append(job)
                seen_urls.add(job['url'])
        
        logger.info(f"Total unique jobs found: {len(unique_jobs)}")
        return unique_jobs
    
    def _extract_jobs_from_json(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract jobs from JSON data in script tags"""
        jobs = []
        
        try:
            # Look for script tags containing job data
            scripts = soup.find_all('script', type='application/json')
            scripts.extend(soup.find_all('script', string=re.compile(r'jobs|careers', re.IGNORECASE)))
            
            for script in scripts:
                try:
                    if script.string:
                        data = json.loads(script.string)
                        if isinstance(data, dict):
                            # Look for job arrays in the JSON
                            job_arrays = self._find_job_arrays_in_json(data)
                            for job_array in job_arrays:
                                for job_data in job_array:
                                    if isinstance(job_data, dict):
                                        job = self._parse_job_from_json(job_data)
                                        if job:
                                            jobs.append(job)
                except (json.JSONDecodeError, ValueError):
                    continue
            
        except Exception as e:
            logger.debug(f"Error extracting jobs from JSON: {e}")
        
        return jobs
    
    def _find_job_arrays_in_json(self, data: dict, path: str = "") -> List[List]:
        """Recursively find arrays that might contain job data"""
        job_arrays = []
        
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            
            if isinstance(value, list):
                # Check if this array contains job-like objects
                if value and isinstance(value[0], dict):
                    # Look for job-like keys
                    first_item = value[0]
                    job_keys = ['title', 'position', 'job_title', 'role', 'name']
                    if any(key in first_item for key in job_keys):
                        job_arrays.append(value)
            
            elif isinstance(value, dict):
                job_arrays.extend(self._find_job_arrays_in_json(value, current_path))
        
        return job_arrays
    
    def _parse_job_from_json(self, job_data: dict) -> Optional[Dict[str, str]]:
        """Parse a job from JSON data"""
        try:
            # Extract title
            title = (job_data.get('title') or 
                    job_data.get('position') or 
                    job_data.get('job_title') or 
                    job_data.get('role') or 
                    job_data.get('name') or 
                    "Unknown Title")
            
            # Extract URL
            url = (job_data.get('url') or 
                  job_data.get('link') or 
                  job_data.get('href') or 
                  job_data.get('apply_url') or 
                  "")
            
            if not url:
                return None
            
            # Make URL absolute
            if url.startswith('/'):
                url = f"https://www.ibm.com{url}"
            elif not url.startswith('http'):
                url = f"https://www.ibm.com/careers/{url}"
            
            # Extract other fields
            location = (job_data.get('location') or 
                       job_data.get('city') or 
                       job_data.get('country') or 
                       self.keyword_05 or "Canada")
            
            team = (job_data.get('team') or 
                   job_data.get('department') or 
                   job_data.get('category') or 
                   self.keyword_08 or "Software Engineering")
            
            # Create unique ID
            job_id = str(hash(url))[-8:]
            unique_id = f"ibm_{job_id}"
            
            return {
                "id": unique_id,
                "company": self.COMPANY_NAME,
                "title": title,
                "team": team,
                "location": location,
                "url": url,
                "description": None,
                "posted_date": None
            }
            
        except Exception as e:
            logger.debug(f"Error parsing job from JSON: {e}")
            return None
    
    def _extract_jobs_from_html(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract jobs from HTML structure"""
        jobs = []
        
        try:
            # Try various selectors for job listings
            selectors = [
                '.search-result',
                '.job-result',
                '.career-result',
                '.job-listing',
                '.result-item',
                '[data-testid*="job"]',
                '[class*="job"]',
                '[class*="result"]'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                if elements:
                    logger.debug(f"Found {len(elements)} elements with selector: {selector}")
                    for element in elements:
                        job = self._parse_job_from_element(element)
                        if job:
                            jobs.append(job)
                    break
            
        except Exception as e:
            logger.debug(f"Error extracting jobs from HTML: {e}")
        
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
                if (('/careers/' in href or '/jobs/' in href) and 
                    text and len(text) > 5 and len(text) < 100):
                    
                    # Make URL absolute
                    if href.startswith('/'):
                        href = f"https://www.ibm.com{href}"
                    elif not href.startswith('http'):
                        href = f"https://www.ibm.com/careers/{href}"
                    
                    # Create job ID
                    job_id = str(hash(href))[-8:]
                    unique_id = f"ibm_{job_id}"
                    
                    job = {
                        "id": unique_id,
                        "company": self.COMPANY_NAME,
                        "title": text,
                        "team": self.keyword_08 or "Software Engineering",
                        "location": self.keyword_05 or "Canada",
                        "url": href,
                        "description": None,
                        "posted_date": None
                    }
                    
                    jobs.append(job)
            
        except Exception as e:
            logger.debug(f"Error extracting jobs from links: {e}")
        
        return jobs
    
    def _parse_job_from_element(self, element) -> Optional[Dict[str, str]]:
        """Parse a job from an HTML element"""
        try:
            # Find the link within the element
            link = element.find('a', href=True)
            if not link:
                return None
            
            href = link.get('href', '')
            title = link.get_text(strip=True)
            
            if not href or not title:
                return None
            
            # Make URL absolute
            if href.startswith('/'):
                href = f"https://www.ibm.com{href}"
            elif not href.startswith('http'):
                href = f"https://www.ibm.com/careers/{href}"
            
            # Create job ID
            job_id = str(hash(href))[-8:]
            unique_id = f"ibm_{job_id}"
            
            return {
                "id": unique_id,
                "company": self.COMPANY_NAME,
                "title": title,
                "team": self.keyword_08 or "Software Engineering",
                "location": self.keyword_05 or "Canada",
                "url": href,
                "description": None,
                "posted_date": None
            }
            
        except Exception as e:
            logger.debug(f"Error parsing job from element: {e}")
            return None


# Convenience function for the scheduler
async def scrape_ibm_v2(keyword_08: Optional[str] = "Software Engineering",
                       keyword_18: Optional[str] = "Internship",
                       keyword_05: Optional[str] = "Canada") -> List[Dict[str, str]]:
    """
    Convenience function to scrape IBM jobs using improved scraper
    
    Args:
        keyword_08: Filter by job function (default: "Software Engineering")
        keyword_18: Filter by job type (default: "Internship")
        keyword_05: Filter by location (default: "Canada")
        
    Returns:
        List of job dictionaries
    """
    scraper = IBMScraperV2(keyword_08=keyword_08, keyword_18=keyword_18, keyword_05=keyword_05)
    return await scraper.scrape()

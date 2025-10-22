"""
BMO Careers Scraper
Scrapes job listings from BMO's career page
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


class BMOScraper:
    """Scraper for BMO careers page"""
    
    BASE_URL = "https://jobs.bmo.com"
    SEARCH_URL = "https://jobs.bmo.com/global/en/search-results"
    COMPANY_NAME = "BMO"
    
    def __init__(
        self, 
        keywords: Optional[List[str]] = None,
        location: Optional[str] = None,
        job_type: Optional[str] = None
    ):
        """
        Initialize the BMO scraper
        
        Args:
            keywords: List of keywords to search for (e.g., ["intern", "internship", "co-op"])
            location: Filter by location (e.g., "Toronto", "Vancouver")
            job_type: Filter by job type (e.g., "Internship", "Co-op")
        """
        self.keywords = keywords or ["intern", "internship", "co-op", "coop"]
        self.location = location
        self.job_type = job_type or "Internship"
        
    def _build_search_params(self, page: int = 1) -> Dict[str, str]:
        """Build the search parameters for BMO careers"""
        params = {
            "keywords": " ".join(self.keywords),
            "location": self.location or "",
            "page": str(page),
            "sortBy": "relevance"
        }
        return params
    
    async def scrape(self) -> List[Dict[str, str]]:
        """
        Scrape all job postings from BMO careers page
        
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
                # First, try to get the search results page
                search_params = self._build_search_params(1)
                logger.info(f"Scraping BMO careers: {self.SEARCH_URL}")
                logger.info(f"Search params: {search_params}")
                
                response = await client.get(self.SEARCH_URL, params=search_params)
                response.raise_for_status()
                
                # Parse the HTML response
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract jobs from the page
                page_jobs = self._extract_jobs_from_html(soup)
                jobs.extend(page_jobs)
                logger.info(f"Scraped {len(page_jobs)} jobs from page 1")
                
                # Check for pagination
                pagination = soup.find('nav', class_='pagination') or soup.find('div', class_='pagination')
                if pagination:
                    # Try to find total pages
                    page_links = pagination.find_all('a', href=True)
                    max_page = 1
                    for link in page_links:
                        try:
                            page_num = int(link.text.strip())
                            max_page = max(max_page, page_num)
                        except ValueError:
                            continue
                    
                    logger.info(f"Found pagination with {max_page} pages")
                    
                    # Scrape remaining pages
                    for page_num in range(2, min(max_page + 1, 10)):  # Limit to 10 pages
                        await asyncio.sleep(1.0)  # Be respectful
                        
                        search_params = self._build_search_params(page_num)
                        logger.info(f"Scraping page {page_num}...")
                        
                        response = await client.get(self.SEARCH_URL, params=search_params)
                        response.raise_for_status()
                        
                        soup = BeautifulSoup(response.text, 'html.parser')
                        page_jobs = self._extract_jobs_from_html(soup)
                        jobs.extend(page_jobs)
                        logger.info(f"Scraped {len(page_jobs)} jobs from page {page_num}")
                        
                        # If no jobs found on this page, stop
                        if not page_jobs:
                            break
                
        except Exception as e:
            logger.error(f"Error scraping BMO: {e}")
            raise
        
        logger.info(f"Total jobs scraped from BMO: {len(jobs)}")
        return jobs
    
    def _extract_jobs_from_html(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract all jobs from the HTML page"""
        jobs = []
        
        try:
            # Look for job listings - BMO might use different selectors
            job_selectors = [
                'div[data-automation-id="jobTitle"]',
                '.job-title',
                '.job-listing',
                '.search-result',
                'article',
                '.job-item',
                '[data-testid="job-card"]',
                '.job-card',
                '.search-result-item'
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
                job_elements = soup.find_all('div', class_=re.compile(r'job|listing|result|card'))
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
                'a[data-automation-id="jobTitle"]',
                '.job-title a',
                'h3 a',
                'h2 a',
                'a[href*="/job/"]',
                '.title a',
                '.job-title',
                'h3',
                'h2'
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
                    if '/job/' in link.get('href', '') or 'careers' in link.get('href', ''):
                        title = link.get_text(strip=True)
                        break
            
            if not title:
                logger.debug("No title found for job element")
                return None
            
            # Extract job URL
            url = None
            url_selectors = [
                'a[data-automation-id="jobTitle"]',
                '.job-title a',
                'h3 a',
                'h2 a',
                'a[href*="/job/"]'
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
                '[data-automation-id="jobLocation"]',
                '.job-location',
                '.location',
                '.job-city',
                '.city',
                '.job-location-text'
            ]
            
            for selector in location_selectors:
                loc_elem = job_element.select_one(selector)
                if loc_elem:
                    location = loc_elem.get_text(strip=True)
                    break
            
            # Extract team/department
            team = None
            team_selectors = [
                '[data-automation-id="jobCategory"]',
                '.job-category',
                '.department',
                '.team',
                '.job-category-text'
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
                id_match = re.search(r'/job/(\d+)', url)
                if id_match:
                    job_id = id_match.group(1)
                else:
                    # Use URL hash as ID
                    job_id = str(hash(url))[-8:]  # Last 8 characters of hash
            
            if not job_id:
                job_id = f"bmo_{hash(url)}"
            
            # Create unique ID with company prefix
            unique_id = f"bmo_{job_id}"
            
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
                "posted_date": None  # BMO doesn't always show posting dates
            }
            
            return job
            
        except Exception as e:
            logger.error(f"Error extracting job data from element: {e}")
            return None


# Convenience function for the scheduler
async def scrape_bmo(
    keywords: Optional[List[str]] = None,
    location: Optional[str] = None,
    job_type: Optional[str] = "Internship"
) -> List[Dict[str, str]]:
    """
    Convenience function to scrape BMO jobs
    
    Args:
        keywords: List of keywords to search for (default: ["intern", "internship", "co-op", "coop"])
        location: Filter by location (optional)
        job_type: Filter by job type (default: "Internship")
        
    Returns:
        List of job dictionaries
    """
    if keywords is None:
        keywords = ["intern", "internship", "co-op", "coop"]
    
    scraper = BMOScraper(
        keywords=keywords,
        location=location,
        job_type=job_type
    )
    return await scraper.scrape()

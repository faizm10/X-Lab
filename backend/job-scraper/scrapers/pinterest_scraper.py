"""
Pinterest Careers Scraper
Scrapes job listings from Pinterest's career page using httpx and BeautifulSoup
"""
import asyncio
from typing import List, Dict, Optional
import httpx
from bs4 import BeautifulSoup
import logging
import re

logger = logging.getLogger(__name__)


class PinterestScraper:
    """Scraper for Pinterest careers page"""
    
    BASE_URL = "https://www.pinterestcareers.com/jobs/"
    COMPANY_NAME = "Pinterest"
    
    def __init__(self, team: Optional[str] = None, employment_type: Optional[str] = None, location: Optional[str] = None):
        """
        Initialize the Pinterest scraper
        
        Args:
            team: Filter by team (e.g., "Engineering", "Design", "Product")
            employment_type: Filter by type (e.g., "Intern", "Regular", "Temporary (Fixed Term)")
            location: Filter by location (e.g., "San Francisco", "Remote", "New York")
        """
        self.team = team
        self.employment_type = employment_type
        self.location = location
        
    def _build_url(self, page: int = 1) -> str:
        """Build the URL with filters and pagination"""
        params = []
        
        if page > 1:
            params.append(f"page={page}")
        
        if self.team:
            params.append(f"team={self.team}")
            
        if self.employment_type:
            params.append(f"type={self.employment_type}")
            
        if self.location:
            params.append(f"location={self.location}")
        
        params.append("pagesize=20")
        
        url = f"{self.BASE_URL}?"
        if params:
            url += "&".join(params)
        
        return url
    
    async def scrape(self) -> List[Dict[str, str]]:
        """
        Scrape all job postings from Pinterest careers page
        
        Returns:
            List of job dictionaries with keys: id, company, title, team, location, url
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
                # Scrape first page
                logger.info(f"Scraping Pinterest careers page: {self._build_url(1)}")
                response = await client.get(self._build_url(1))
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract total pages
                total_pages = self._get_total_pages(soup)
                logger.info(f"Found {total_pages} page(s) to scrape")
                
                # Extract jobs from first page
                page_jobs = self._extract_jobs_from_page(soup)
                jobs.extend(page_jobs)
                logger.info(f"Scraped {len(page_jobs)} jobs from page 1")
                
                # Scrape remaining pages
                for page_num in range(2, total_pages + 1):
                    await asyncio.sleep(0.5)  # Be respectful
                    
                    logger.info(f"Scraping page {page_num}...")
                    response = await client.get(self._build_url(page_num))
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    page_jobs = self._extract_jobs_from_page(soup)
                    jobs.extend(page_jobs)
                    logger.info(f"Scraped {len(page_jobs)} jobs from page {page_num}")
                
        except Exception as e:
            logger.error(f"Error scraping Pinterest: {e}")
            raise
        
        logger.info(f"Total jobs scraped from Pinterest: {len(jobs)}")
        return jobs
    
    def _get_total_pages(self, soup: BeautifulSoup) -> int:
        """Get the total number of pages from pagination"""
        try:
            # Find pagination links
            pagination = soup.find('nav', attrs={'aria-label': 'Pagination'})
            if not pagination:
                # Check if there are any jobs
                job_count = soup.find('strong', string=re.compile(r'matching jobs'))
                return 1 if job_count else 0
            
            # Find all page links
            page_links = pagination.find_all('a', href=re.compile(r'page='))
            if not page_links:
                return 1
            
            # Extract page numbers
            max_page = 1
            for link in page_links:
                href = link.get('href', '')
                match = re.search(r'page=(\d+)', href)
                if match:
                    page_num = int(match.group(1))
                    max_page = max(max_page, page_num)
            
            return max_page
            
        except Exception as e:
            logger.warning(f"Could not determine total pages: {e}")
            return 1
    
    def _extract_jobs_from_page(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract all jobs from the current page"""
        jobs = []
        
        try:
            # Find main content area
            main = soup.find('main')
            if not main:
                logger.warning("Could not find main content area")
                return jobs
            
            # Find all job headings with links
            job_headings = main.find_all('h2')
            
            for heading in job_headings:
                try:
                    # Find the link within the heading
                    link = heading.find('a', href=re.compile(r'/jobs/'))
                    if not link:
                        continue
                    
                    # Get job URL
                    job_url = link.get('href', '')
                    if not job_url:
                        continue
                    
                    # Make URL absolute
                    if job_url.startswith('/'):
                        job_url = f"https://www.pinterestcareers.com{job_url}"
                    
                    # Extract job ID from URL
                    job_id = None
                    if 'gh_jid=' in job_url:
                        match = re.search(r'gh_jid=(\d+)', job_url)
                        if match:
                            job_id = match.group(1)
                    elif '/jobs/' in job_url:
                        match = re.search(r'/jobs/(\d+)/', job_url)
                        if match:
                            job_id = match.group(1)
                    
                    if not job_id:
                        logger.warning(f"Could not extract job ID from URL: {job_url}")
                        continue
                    
                    # Get job title
                    title = link.get_text(strip=True)
                    if not title:
                        title = "Unknown Title"
                    
                    # Find the parent div containing location and team info
                    parent = heading.find_parent('div')
                    location = None
                    team = None
                    
                    if parent:
                        # Find the list items (location and team)
                        list_items = parent.find_all('li')
                        items_text = [item.get_text(strip=True) for item in list_items if item.get_text(strip=True)]
                        
                        # First item is usually location, second is team
                        if len(items_text) >= 1:
                            location = items_text[0]
                        if len(items_text) >= 2:
                            team = items_text[1]
                    
                    # Create unique ID with company prefix
                    unique_id = f"pinterest_{job_id}"
                    
                    job = {
                        "id": unique_id,
                        "company": self.COMPANY_NAME,
                        "title": title,
                        "team": team,
                        "location": location,
                        "url": job_url,
                        "description": None  # Description would require visiting individual job pages
                    }
                    
                    jobs.append(job)
                    logger.debug(f"Extracted job: {title} ({unique_id})")
                    
                except Exception as e:
                    logger.error(f"Error extracting job from heading: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error extracting jobs from page: {e}")
        
        return jobs


# Convenience function for the scheduler
async def scrape_pinterest(team: Optional[str] = "Engineering", 
                          employment_type: Optional[str] = None,
                          location: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Convenience function to scrape Pinterest jobs
    
    Args:
        team: Filter by team (default: "Engineering")
        employment_type: Filter by employment type
        location: Filter by location
        
    Returns:
        List of job dictionaries
    """
    scraper = PinterestScraper(team=team, employment_type=employment_type, location=location)
    return await scraper.scrape()


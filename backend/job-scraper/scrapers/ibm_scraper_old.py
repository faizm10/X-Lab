"""
IBM Careers Scraper
Scrapes job listings from IBM's career page using httpx and BeautifulSoup
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


class IBMScraper:
    """Scraper for IBM careers page"""
    
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
        
    def _build_url(self, page: int = 1) -> str:
        """Build the URL with filters and pagination"""
        params = []
        
        if self.keyword_08:
            params.append(f"field_keyword_08[0]={self.keyword_08.replace(' ', '%20')}")
        if self.keyword_18:
            params.append(f"field_keyword_18[0]={self.keyword_18.replace(' ', '%20')}")
        if self.keyword_05:
            params.append(f"field_keyword_05[0]={self.keyword_05.replace(' ', '%20')}")
        
        # Add pagination if not first page
        if page > 1:
            params.append(f"page={page}")
        
        url = f"{self.BASE_URL}?"
        if params:
            url += "&".join(params)
        
        return url
    
    async def _extract_posting_date(self, client: httpx.AsyncClient, job_url: str) -> Optional[datetime]:
        """
        Extract posting date from individual job detail page
        """
        try:
            response = await client.get(job_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for JSON-LD structured data first
            scripts = soup.find_all('script', type='application/ld+json')
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    if isinstance(data, dict) and 'datePosted' in data:
                        date_str = data['datePosted']
                        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                except (json.JSONDecodeError, ValueError) as e:
                    logger.debug(f"Could not parse JSON-LD: {e}")
                    continue
            
            # Fallback: Look for date patterns in the HTML
            date_patterns = [
                r'Posted\s+on\s+(\d{4}-\d{2}-\d{2})',
                r'Date\s+Posted:\s*(\d{4}-\d{2}-\d{2})',
                r'(\d{4}-\d{2}-\d{2})',
            ]
            
            page_text = soup.get_text()
            for pattern in date_patterns:
                match = re.search(pattern, page_text)
                if match:
                    try:
                        return datetime.fromisoformat(match.group(1))
                    except ValueError:
                        continue
            
            logger.warning(f"No posting date found for {job_url}")
            return None
            
        except Exception as e:
            logger.warning(f"Error extracting posting date from {job_url}: {e}")
            return None
    
    async def scrape(self) -> List[Dict[str, str]]:
        """
        Scrape all job postings from IBM careers page
        
        Returns:
            List of job dictionaries with keys: id, company, title, team, location, url, posted_date
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
                logger.info(f"Scraping IBM careers page: {self._build_url(1)}")
                response = await client.get(self._build_url(1))
                response.raise_for_status()
                
                logger.debug(f"Response status: {response.status_code}")
                logger.debug(f"Response length: {len(response.text)} characters")
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Debug: Log some page content
                page_title = soup.find('title')
                if page_title:
                    logger.debug(f"Page title: {page_title.get_text()}")
                
                # Debug: Check if we're getting the expected content
                page_text = soup.get_text()
                if 'software engineer' in page_text.lower():
                    logger.debug("Found 'software engineer' text in page")
                else:
                    logger.warning("Did not find 'software engineer' text in page")
                
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
                
                # Now fetch posting dates from individual job pages
                logger.info(f"Fetching posting dates for {len(jobs)} jobs...")
                for i, job in enumerate(jobs):
                    if i > 0 and i % 5 == 0:
                        logger.info(f"Processed {i}/{len(jobs)} job detail pages...")
                        await asyncio.sleep(0.5)  # Be respectful with rate limiting
                    
                    posted_date = await self._extract_posting_date(client, job['url'])
                    job['posted_date'] = posted_date
                    
                    await asyncio.sleep(0.2)  # Small delay between requests
                
        except Exception as e:
            logger.error(f"Error scraping IBM: {e}")
            raise
        
        logger.info(f"Total jobs scraped from IBM: {len(jobs)}")
        jobs_with_dates = sum(1 for j in jobs if j.get('posted_date'))
        logger.info(f"Jobs with posting dates: {jobs_with_dates}/{len(jobs)}")
        return jobs
    
    def _get_total_pages(self, soup: BeautifulSoup) -> int:
        """Get the total number of pages from pagination"""
        try:
            # Look for pagination elements
            pagination_selectors = [
                '.pagination',
                '[data-testid="pagination"]',
                '.pager',
                '.search-results-pagination'
            ]
            
            pagination = None
            for selector in pagination_selectors:
                pagination = soup.select_one(selector)
                if pagination:
                    break
            
            if not pagination:
                # Check if there are any job results
                job_results = soup.select('.job-result, .search-result, .job-listing')
                return 1 if job_results else 0
            
            # Find all page links
            page_links = pagination.find_all('a', href=True)
            if not page_links:
                return 1
            
            # Extract page numbers from hrefs
            max_page = 1
            for link in page_links:
                href = link.get('href', '')
                # Look for page parameter in URL
                if 'page=' in href:
                    match = re.search(r'page=(\d+)', href)
                    if match:
                        page_num = int(match.group(1))
                        max_page = max(max_page, page_num)
                
                # Also check link text for page numbers
                link_text = link.get_text(strip=True)
                if link_text.isdigit():
                    page_num = int(link_text)
                    max_page = max(max_page, page_num)
            
            return max_page
            
        except Exception as e:
            logger.warning(f"Could not determine total pages: {e}")
            return 1
    
    def _extract_jobs_from_page(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract all jobs from the current page"""
        jobs = []
        
        try:
            # IBM-specific selectors based on their career page structure
            job_selectors = [
                '.search-result-item',
                '.job-result-item', 
                '.career-search-result',
                '.search-result',
                '.job-listing',
                '.result-item',
                '[data-testid="job-result"]',
                '.job-card',
                '.job-item'
            ]
            
            job_elements = []
            for selector in job_selectors:
                job_elements = soup.select(selector)
                if job_elements:
                    logger.debug(f"Found jobs using selector: {selector}")
                    break
            
            if not job_elements:
                # Fallback: look for any links that might be job postings
                job_elements = soup.find_all('a', href=re.compile(r'/careers/|/jobs/|careers\.ibm\.com'))
                job_elements = [elem for elem in job_elements if elem.get_text(strip=True)]
                logger.debug(f"Found {len(job_elements)} potential job links as fallback")
            
            if not job_elements:
                # Another fallback: look for any div containing job-related text
                page_text = soup.get_text()
                if 'software engineer' in page_text.lower() or 'internship' in page_text.lower():
                    # Try to find any structured content
                    job_elements = soup.find_all(['div', 'article', 'section'], 
                                               string=re.compile(r'software engineer|intern|developer', re.IGNORECASE))
                    logger.debug(f"Found {len(job_elements)} potential job elements from text search")
            
            for job_element in job_elements:
                try:
                    job_data = self._extract_job_from_element(job_element)
                    if job_data:
                        jobs.append(job_data)
                        
                except Exception as e:
                    logger.error(f"Error extracting job from element: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error extracting jobs from page: {e}")
        
        return jobs
    
    def _extract_job_from_element(self, element) -> Optional[Dict[str, str]]:
        """Extract job data from a single job element"""
        try:
            # Find the job link
            link = element
            if element.name != 'a':
                link = element.find('a', href=True)
            
            if not link or not link.get('href'):
                return None
            
            job_url = link.get('href')
            if not job_url:
                return None
            
            # Make URL absolute
            if job_url.startswith('/'):
                job_url = urljoin(self.BASE_URL, job_url)
            elif not job_url.startswith('http'):
                job_url = f"https://www.ibm.com{job_url}"
            
            # Extract job ID from URL
            job_id = None
            if '/jobs/' in job_url:
                match = re.search(r'/jobs/([^/]+)', job_url)
                if match:
                    job_id = match.group(1)
            elif 'jobId=' in job_url:
                match = re.search(r'jobId=([^&]+)', job_url)
                if match:
                    job_id = match.group(1)
            
            if not job_id:
                # Create ID from URL hash
                job_id = str(hash(job_url))[-8:]  # Last 8 chars of hash
            
            # Get job title
            title = link.get_text(strip=True)
            if not title:
                # Try to find title in child elements
                title_elem = element.find(['h1', 'h2', 'h3', 'h4', '.title', '.job-title'])
                if title_elem:
                    title = title_elem.get_text(strip=True)
                else:
                    title = "Unknown Title"
            
            # Find location and other details
            location = self.keyword_05 or "Canada"  # Default to Canada
            team = self.keyword_08 or "Software Engineering"
            
            # Try to extract more specific location/team from the element
            text_content = element.get_text()
            
            # Look for location patterns
            location_patterns = [
                r'(Toronto|Vancouver|Montreal|Ottawa|Calgary|Edmonton|Winnipeg|Halifax)',
                r'(Remote|Hybrid|On-site)',
            ]
            
            for pattern in location_patterns:
                match = re.search(pattern, text_content, re.IGNORECASE)
                if match:
                    location = match.group(1)
                    break
            
            # Look for team/role patterns
            team_patterns = [
                r'(Software Engineer|Developer|Intern|Co-op)',
                r'(Frontend|Backend|Full Stack|Mobile)',
            ]
            
            for pattern in team_patterns:
                match = re.search(pattern, text_content, re.IGNORECASE)
                if match:
                    team = match.group(1)
                    break
            
            # Create unique ID with company prefix
            unique_id = f"ibm_{job_id}"
            
            job = {
                "id": unique_id,
                "company": self.COMPANY_NAME,
                "title": title,
                "team": team,
                "location": location,
                "url": job_url,
                "description": None,  # Description would require visiting individual job pages
                "posted_date": None  # Will be fetched from job detail page
            }
            
            logger.debug(f"Extracted job: {title} ({unique_id})")
            return job
            
        except Exception as e:
            logger.error(f"Error extracting job from element: {e}")
            return None


# Convenience function for the scheduler
async def scrape_ibm(keyword_08: Optional[str] = "Software Engineering",
                    keyword_18: Optional[str] = "Internship",
                    keyword_05: Optional[str] = "Canada") -> List[Dict[str, str]]:
    """
    Convenience function to scrape IBM jobs
    
    Args:
        keyword_08: Filter by job function (default: "Software Engineering")
        keyword_18: Filter by job type (default: "Internship")
        keyword_05: Filter by location (default: "Canada")
        
    Returns:
        List of job dictionaries
    """
    scraper = IBMScraper(keyword_08=keyword_08, keyword_18=keyword_18, keyword_05=keyword_05)
    return await scraper.scrape()

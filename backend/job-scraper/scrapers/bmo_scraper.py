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
from playwright.async_api import async_playwright

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
            "location": self.location or "Ontario",  # Default to Ontario as requested
            "page": str(page),
            "sortBy": "relevance",
            "department": "Technology",  # Filter for Technology department
            "jobType": "Intern (Fixed Term)"  # Filter for Intern positions
        }
        return params
    
    async def scrape(self) -> List[Dict[str, str]]:
        """
        Scrape all job postings from BMO careers page using Playwright
        
        Returns:
            List of job dictionaries with keys: id, company, title, team, location, url
        """
        jobs = []
        
        try:
            async with async_playwright() as p:
                # Launch browser
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
                page = await context.new_page()
                
                # Build the search URL with parameters
                search_params = self._build_search_params(1)
                search_url = f"{self.SEARCH_URL}?" + "&".join([f"{k}={v}" for k, v in search_params.items() if v])
                
                logger.info(f"Scraping BMO careers: {search_url}")
                
                # Navigate to the page
                await page.goto(search_url, wait_until="networkidle")
                
                # Wait for job listings to load
                try:
                    await page.wait_for_selector('[data-automation-id="jobTitle"], .job-title, .search-result, article', timeout=10000)
                except:
                    logger.warning("No job selectors found, trying alternative approach")
                
                # Get the page content
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Extract jobs from the page
                page_jobs = self._extract_jobs_from_html(soup)
                jobs.extend(page_jobs)
                logger.info(f"Scraped {len(page_jobs)} jobs from page 1")
                
                # Check for pagination and scrape additional pages
                try:
                    # Look for pagination
                    pagination_selectors = [
                        'nav[aria-label="pagination"]',
                        '.pagination',
                        '[data-automation-id="pagination"]',
                        'nav[role="navigation"]'
                    ]
                    
                    pagination_found = False
                    for selector in pagination_selectors:
                        if await page.locator(selector).count() > 0:
                            pagination_found = True
                            break
                    
                    if pagination_found:
                        # Try to find and click next page
                        next_button = page.locator('a[aria-label="Next"], button[aria-label="Next"], .next, [data-automation-id="next"]')
                        if await next_button.count() > 0:
                            await next_button.click()
                            await page.wait_for_load_state("networkidle")
                            
                            # Extract jobs from next page
                            content = await page.content()
                            soup = BeautifulSoup(content, 'html.parser')
                            page_jobs = self._extract_jobs_from_html(soup)
                            jobs.extend(page_jobs)
                            logger.info(f"Scraped {len(page_jobs)} jobs from page 2")
                            
                except Exception as e:
                    logger.warning(f"Pagination handling failed: {e}")
                
                await browser.close()
                
        except Exception as e:
            logger.error(f"Error scraping BMO: {e}")
            raise
        
        logger.info(f"Total jobs scraped from BMO: {len(jobs)}")
        return jobs
    
    def _extract_jobs_from_html(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract all jobs from the HTML page"""
        jobs = []
        
        try:
            # Look for job listings - BMO uses dynamic content, so we need broader selectors
            job_selectors = [
                'div[data-automation-id="jobTitle"]',
                '.job-title',
                '.job-listing',
                '.search-result',
                'article',
                '.job-item',
                '[data-testid="job-card"]',
                '.job-card',
                '.search-result-item',
                # BMO-specific selectors
                '[data-automation-id*="job"]',
                '[data-testid*="job"]',
                '.css-1q2dra3',  # Common BMO selector
                '.css-19uc56f',  # Common BMO selector
                'div[class*="job"]',
                'div[class*="result"]',
                'div[class*="card"]',
                'div[class*="item"]'
            ]
            
            job_elements = []
            seen_ids = set()
            for selector in job_selectors:
                elements = soup.select(selector)
                if elements:
                    job_elements = elements
                    logger.info(f"Found {len(elements)} job elements using selector: {selector}")
                    break
            
            if not job_elements:
                # Fallback: look for any div with job-related classes or attributes
                job_elements = soup.find_all('div', class_=re.compile(r'job|listing|result|card|item'))
                logger.info(f"Fallback: Found {len(job_elements)} potential job elements")
                
                # Also try to find any elements with job-related data attributes
                if not job_elements:
                    job_elements = soup.find_all(attrs={'data-automation-id': re.compile(r'job|title|result', re.IGNORECASE)})
                    logger.info(f"Data attributes fallback: Found {len(job_elements)} potential job elements")
            
            for job_element in job_elements:
                try:
                    job_data = self._extract_job_data(job_element)
                    if job_data:
                        job_id = job_data.get("id")
                        if job_id and job_id in seen_ids:
                            logger.debug("Skipping duplicate job id %s", job_id)
                            continue

                        jobs.append(job_data)
                        if job_id:
                            seen_ids.add(job_id)
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
                # Try to extract job ID from URL (alphanumeric slug)
                id_match = re.search(r"/job/([^/]+)", url)
                if id_match:
                    job_id = id_match.group(1).lower()
                else:
                    # Use deterministic hash of URL for fallback
                    job_id = re.sub(r"[^a-z0-9]+", "-", url.lower()).strip("-")[-12:]
            
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

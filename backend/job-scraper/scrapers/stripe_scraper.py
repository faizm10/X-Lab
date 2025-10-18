import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StripeScraper:
    """Scraper for Stripe job postings"""
    
    BASE_URL = "https://stripe.com/jobs/search"
    COMPANY_NAME = "Stripe"
    
    # Keywords to search for on Stripe's job board (intern only)
    SEARCH_KEYWORDS = [
        "intern"
    ]
    
    # Canadian cities to filter for
    CANADA_LOCATIONS = [
        "toronto",
        "vancouver", 
        "ottawa",
        "montreal",
        "calgary",
        "edmonton",
        "canada",
        "remote in canada"
    ]
    
    def __init__(self):
        self.jobs: List[Dict] = []
    
    def _is_canada_location(self, location: str) -> bool:
        """Check if location is in Canada"""
        if not location:
            return False
        location_lower = location.lower()
        return any(city in location_lower for city in self.CANADA_LOCATIONS)
    
    def _contains_exact_keyword(self, title: str, keyword: str) -> bool:
        """Check if title contains the exact keyword with word boundaries"""
        import re
        pattern = r'\b' + re.escape(keyword) + r'\b'
        return bool(re.search(pattern, title, re.IGNORECASE))
    
    async def scrape(self, keywords: List[str] = None) -> List[Dict]:
        """
        Scrape Stripe job postings by searching for specific keywords
        
        Args:
            keywords: List of search keywords (default: uses SEARCH_KEYWORDS)
            
        Returns:
            List of job posting dictionaries (deduplicated)
        """
        if keywords is None:
            keywords = self.SEARCH_KEYWORDS
        
        logger.info(f"Starting Stripe scrape with keywords: {keywords}")
        all_jobs = {}  # Use dict to deduplicate by job ID
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                # Search for each keyword separately
                for keyword in keywords:
                    logger.info(f"Searching for: {keyword}")
                    
                    try:
                        # Navigate to jobs page with query
                        url = f"{self.BASE_URL}?query={keyword}"
                        logger.info(f"Navigating to: {url}")
                        await page.goto(url, wait_until="networkidle", timeout=30000)
                        
                        # Wait for job listings to load
                        await page.wait_for_selector("table", timeout=10000)
                        
                        # Get page content
                        content = await page.content()
                        soup = BeautifulSoup(content, 'html.parser')
                        
                        # Find job listings table
                        table = soup.find('table')
                        if not table:
                            logger.warning(f"No job table found for keyword: {keyword}")
                            continue
                        
                        # Parse job rows
                        rows = table.find('tbody').find_all('tr') if table.find('tbody') else []
                        logger.info(f"Found {len(rows)} job rows for keyword '{keyword}'")
                        
                        for row in rows:
                            try:
                                job_data = self._parse_job_row(row)
                                if job_data:
                                    # Filter: Only Canada locations AND exact keyword match
                                    if (self._is_canada_location(job_data.get('location')) and 
                                        self._contains_exact_keyword(job_data.get('title'), keyword)):
                                        # Use job ID as key to avoid duplicates
                                        job_id = job_data['id']
                                        if job_id not in all_jobs:
                                            all_jobs[job_id] = job_data
                                            logger.info(f"Added: {job_data['title']} - {job_data['location']}")
                                    else:
                                        if not self._is_canada_location(job_data.get('location')):
                                            logger.debug(f"Filtered out (non-Canada): {job_data['title']} - {job_data['location']}")
                                        elif not self._contains_exact_keyword(job_data.get('title'), keyword):
                                            logger.debug(f"Filtered out (no exact '{keyword}'): {job_data['title']} - {job_data['location']}")
                            except Exception as e:
                                logger.error(f"Error parsing job row: {e}")
                                continue
                        
                        # Small delay between searches to be respectful
                        await asyncio.sleep(1)
                        
                    except PlaywrightTimeout as e:
                        logger.error(f"Timeout while scraping keyword '{keyword}': {e}")
                        continue
                    except Exception as e:
                        logger.error(f"Error during scraping keyword '{keyword}': {e}")
                        continue
                
                self.jobs = list(all_jobs.values())
                logger.info(f"Successfully scraped {len(self.jobs)} unique jobs across all keywords")
                
            except Exception as e:
                logger.error(f"Error during scraping: {e}")
            finally:
                await browser.close()
        
        return self.jobs
    
    def _parse_job_row(self, row) -> Dict:
        """Parse a single job row from the table"""
        try:
            cells = row.find_all('td')
            if len(cells) < 3:
                return None
            
            # Extract job link and title
            link_tag = cells[0].find('a')
            if not link_tag:
                return None
            
            job_url = link_tag.get('href', '')
            if not job_url.startswith('http'):
                job_url = f"https://stripe.com{job_url}"
            
            title = link_tag.get_text(strip=True)
            
            # Extract job ID from URL
            job_id = job_url.split('/')[-1] if '/' in job_url else None
            if not job_id:
                return None
            
            # Extract team
            team = cells[1].get_text(strip=True) if len(cells) > 1 else None
            
            # Extract location
            location = cells[2].get_text(strip=True) if len(cells) > 2 else None
            
            # Create unique ID by combining job_id and location
            # This handles jobs posted in multiple locations
            location_slug = location.lower().replace(' ', '-').replace(',', '') if location else 'unknown'
            unique_id = f"stripe-{job_id}-{location_slug}"
            
            job_data = {
                "id": unique_id,
                "company": self.COMPANY_NAME,
                "title": title,
                "team": team,
                "location": location,
                "url": job_url,
                "description": None,  # Would need to visit individual page
                "posted_date": datetime.utcnow(),
            }
            
            return job_data
            
        except Exception as e:
            logger.error(f"Error parsing job row: {e}")
            return None


async def test_scraper():
    """Test the scraper"""
    scraper = StripeScraper()
    jobs = await scraper.scrape()
    print(f"\nFound {len(jobs)} jobs:")
    for job in jobs[:10]:  # Print first 10
        print(f"  - {job['title']} ({job['location']})")


if __name__ == "__main__":
    asyncio.run(test_scraper())


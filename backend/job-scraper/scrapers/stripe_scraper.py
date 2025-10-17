import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StripeScraper:
    """Scraper for Stripe job postings"""
    
    BASE_URL = "https://stripe.com/jobs/search"
    COMPANY_NAME = "Stripe"
    
    def __init__(self):
        self.jobs: List[Dict] = []
    
    async def scrape(self, query: str = "intern") -> List[Dict]:
        """
        Scrape Stripe job postings
        
        Args:
            query: Search query (default: "intern")
            
        Returns:
            List of job posting dictionaries
        """
        logger.info(f"Starting Stripe scrape with query: {query}")
        self.jobs = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                # Navigate to jobs page with query
                url = f"{self.BASE_URL}?query={query}"
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
                    logger.warning("No job table found")
                    await browser.close()
                    return []
                
                # Parse job rows
                rows = table.find('tbody').find_all('tr') if table.find('tbody') else []
                logger.info(f"Found {len(rows)} job rows")
                
                for row in rows:
                    try:
                        job_data = self._parse_job_row(row)
                        if job_data:
                            self.jobs.append(job_data)
                    except Exception as e:
                        logger.error(f"Error parsing job row: {e}")
                        continue
                
                logger.info(f"Successfully scraped {len(self.jobs)} jobs")
                
            except PlaywrightTimeout as e:
                logger.error(f"Timeout while scraping: {e}")
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
            
            job_data = {
                "id": f"stripe-{job_id}",
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
    jobs = await scraper.scrape("intern")
    print(f"\nFound {len(jobs)} jobs:")
    for job in jobs[:5]:  # Print first 5
        print(f"  - {job['title']} ({job['location']})")


if __name__ == "__main__":
    asyncio.run(test_scraper())


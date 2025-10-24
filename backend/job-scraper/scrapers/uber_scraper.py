import asyncio
from typing import List, Dict, Optional
import logging
from datetime import datetime
import httpx
from bs4 import BeautifulSoup
import re
from playwright.async_api import async_playwright, Page

logger = logging.getLogger(__name__)

class UberScraper:
    """
    Scraper for Uber careers page using Playwright.
    Fetches internship and university program job postings.
    """
    BASE_URL = "https://www.uber.com"
    CAREERS_URL = "https://www.uber.com/ca/en/careers/list/"
    COMPANY_NAME = "Uber"

    def __init__(
        self,
        department: Optional[str] = None,
        team: Optional[str] = None,
        location: Optional[str] = None
    ):
        """
        Initialize the Uber scraper.
        
        Args:
            department: Department filter (e.g., "University")
            team: Team filter (e.g., "Engineering")
            location: Location filter (optional)
        """
        self.department = department or "University"
        self.team = team or "Engineering"
        self.location = location

    def _build_url(self) -> str:
        """
        Build the careers URL with filters.
        
        Returns:
            URL string with query parameters
        """
        params = []
        
        if self.department:
            params.append(f"department={self.department}")
        
        if self.team:
            params.append(f"team={self.team}")
        
        if self.location:
            params.append(f"location={self.location}")
        
        if params:
            return f"{self.CAREERS_URL}?{'&'.join(params)}"
        
        return self.CAREERS_URL

    async def scrape(self) -> List[Dict[str, str]]:
        """
        Scrape job postings from Uber careers page.
        
        Returns:
            List of job dictionaries with keys: id, company, title, team, location, url, description, posted_date
        """
        jobs = []
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                try:
                    url = self._build_url()
                    logger.info(f"Navigating to {url}")
                    
                    await page.goto(url, wait_until="networkidle", timeout=30000)
                    
                    # Wait for job listings to load
                    await page.wait_for_selector('a[href^="/careers/list/"]', timeout=10000)
                    
                    # Extract jobs from the page
                    jobs = await self._extract_jobs_from_page(page)
                    
                    logger.info(f"Total jobs scraped from Uber: {len(jobs)}")
                    
                except Exception as e:
                    logger.error(f"Error during scraping: {e}")
                    raise
                finally:
                    await browser.close()
                
        except Exception as e:
            logger.error(f"Error scraping Uber: {e}")
            raise
        
        return jobs

    async def _extract_jobs_from_page(self, page: Page) -> List[Dict[str, str]]:
        """
        Extract job information from the page.
        
        Args:
            page: Playwright page object
            
        Returns:
            List of job dictionaries
        """
        jobs = []
        
        try:
            # Execute JavaScript to extract job data
            job_data = await page.evaluate("""
                () => {
                    const jobElements = document.querySelectorAll('a[href^="/careers/list/"]');
                    const jobs = [];
                    
                    jobElements.forEach(link => {
                        const href = link.getAttribute('href');
                        const title = link.textContent.trim();
                        
                        // Find the parent container to get other details
                        let container = link.closest('div');
                        if (container) {
                            container = container.parentElement;
                        }
                        
                        // Try to find location and team info
                        let locations = [];
                        let team = '';
                        
                        if (container) {
                            // Find all generic divs in the container
                            const sections = container.querySelectorAll('div');
                            
                            sections.forEach((section, idx) => {
                                const text = section.textContent.trim();
                                
                                // Check if this is the team section
                                if (text === 'Sub-Team') {
                                    // Get the next section which should contain the team name
                                    const nextSection = sections[idx + 1];
                                    if (nextSection) {
                                        team = nextSection.textContent.trim();
                                    }
                                }
                                
                                // Check if this is the location section
                                if (text === 'Location') {
                                    // Get the next section which should contain locations
                                    const nextSection = sections[idx + 1];
                                    if (nextSection) {
                                        // Find all location divs
                                        const locationDivs = nextSection.querySelectorAll('div');
                                        locationDivs.forEach(locDiv => {
                                            const locText = locDiv.textContent.trim();
                                            if (locText && locText !== 'Location' && locText !== 'Multiple Locations') {
                                                locations.push(locText);
                                            }
                                        });
                                        
                                        // If no locations found in divs, check the section text
                                        if (locations.length === 0) {
                                            const locText = nextSection.textContent.trim();
                                            if (locText && locText !== 'Location') {
                                                locations.push(locText);
                                            }
                                        }
                                    }
                                }
                            });
                        }
                        
                        if (title && href) {
                            jobs.push({
                                title: title,
                                url: href,
                                team: team,
                                locations: locations
                            });
                        }
                    });
                    
                    return jobs;
                }
            """)
            
            # Process the extracted data
            for job_info in job_data:
                try:
                    # Extract job ID from URL
                    url = job_info.get("url", "")
                    match = re.search(r'/careers/list/(\d+)', url)
                    if not match:
                        continue
                    
                    job_id = match.group(1)
                    
                    # Build full URL
                    job_url = f"{self.BASE_URL}{url}"
                    
                    # Get title
                    title = job_info.get("title", "").strip()
                    if not title:
                        continue
                    
                    # Get team
                    team = job_info.get("team", "") or self.team
                    
                    # Get location(s)
                    locations = job_info.get("locations", [])
                    if locations:
                        location = ", ".join(locations)
                    else:
                        location = "Multiple Locations"
                    
                    job_dict = {
                        "id": f"uber_{job_id}",
                        "company": self.COMPANY_NAME,
                        "title": title,
                        "team": team,
                        "location": location,
                        "url": job_url,
                        "description": "",  # Description would require visiting each job page
                        "posted_date": None  # Posted date not available on listing page
                    }
                    
                    jobs.append(job_dict)
                    logger.debug(f"Extracted job: {title} - {location}")
                
                except Exception as e:
                    logger.error(f"Error processing job data: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error extracting jobs from page: {e}")
        
        return jobs


async def main():
    """Test the Uber scraper."""
    scraper = UberScraper(department="University", team="Engineering")
    jobs = await scraper.scrape()
    
    print(f"\nFound {len(jobs)} Uber jobs:")
    for job in jobs:
        print(f"\n- {job['title']}")
        print(f"  Team: {job['team']}")
        print(f"  Location: {job['location']}")
        print(f"  URL: {job['url']}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())


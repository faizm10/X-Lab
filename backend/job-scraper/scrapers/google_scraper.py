import asyncio
from typing import List, Dict, Optional
import logging
from datetime import datetime
import httpx
from bs4 import BeautifulSoup
import re
from playwright.async_api import async_playwright, Page

logger = logging.getLogger(__name__)

class GoogleScraper:
    """
    Scraper for Google careers page using Playwright.
    Fetches software developer intern job postings.
    """
    BASE_URL = "https://www.google.com"
    CAREERS_URL = "https://www.google.com/about/careers/applications/jobs/results/"
    COMPANY_NAME = "Google"

    def __init__(
        self,
        employment_type: str = "INTERN",
        target_level: str = "INTERN_AND_APPRENTICE",
        search_query: str = "Software Developer",
        locations: List[str] = None
    ):
        """
        Initialize the Google scraper.
        
        Args:
            employment_type: Type of employment (default: "INTERN")
            target_level: Target experience level (default: "INTERN_AND_APPRENTICE")
            search_query: Search query for jobs (default: "Software Developer")
            locations: List of locations to search (default: ["Canada", "United States"])
        """
        self.employment_type = employment_type
        self.target_level = target_level
        self.search_query = search_query
        self.locations = locations or ["Canada", "United States"]

    def _build_url(self) -> str:
        """
        Build the careers URL with filters.
        
        Returns:
            URL string with query parameters
        """
        params = {
            "distance": "50",
            "employment_type": self.employment_type,
            "target_level": self.target_level,
            "q": f'"{self.search_query}"'
        }
        
        # Add location parameters - each location needs its own parameter
        for i, location in enumerate(self.locations):
            params[f"location"] = location
        
        # Add company parameters for Google and its subsidiaries
        companies = ["GFiber", "Wing", "Verily Life Sciences", "Waymo", "X", "Fitbit", "Google", "YouTube"]
        for company in companies:
            params[f"company"] = company
        
        # Build query string
        query_parts = []
        
        # Add basic parameters
        for key, value in params.items():
            if key not in ["location", "company"]:  # Handle these separately
                query_parts.append(f"{key}={value}")
        
        # Add location parameters (each location gets its own parameter)
        for location in self.locations:
            query_parts.append(f"location={location}")
        
        # Add company parameters (each company gets its own parameter)
        companies = ["GFiber", "Wing", "Verily Life Sciences", "Waymo", "X", "Fitbit", "Google", "YouTube"]
        for company in companies:
            query_parts.append(f"company={company}")
        
        return f"{self.CAREERS_URL}?{'&'.join(query_parts)}"

    async def scrape(self) -> List[Dict[str, str]]:
        """
        Scrape job postings from Google careers page.
        
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
                    
                    # Wait for job listings to load - try multiple selectors
                    try:
                        await page.wait_for_selector('[data-testid="job-card"]', timeout=5000)
                    except:
                        try:
                            await page.wait_for_selector('.job-card', timeout=5000)
                        except:
                            try:
                                await page.wait_for_selector('h3', timeout=5000)  # Job titles are in h3 elements
                            except:
                                logger.warning("Could not find job card selector, proceeding with extraction")
                    
                    # Extract jobs from the page
                    jobs = await self._extract_jobs_from_page(page)
                    
                    logger.info(f"Total jobs scraped from Google: {len(jobs)}")
                    
                except Exception as e:
                    logger.error(f"Error during scraping: {e}")
                    raise
                finally:
                    await browser.close()
                
        except Exception as e:
            logger.error(f"Error scraping Google: {e}")
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
            # Execute JavaScript to extract job data with multiple fallback strategies
            job_data = await page.evaluate("""
                () => {
                    const jobs = [];
                    
                    // Strategy 1: Look for job cards with data-testid
                    let jobElements = document.querySelectorAll('[data-testid="job-card"]');
                    
                    // Strategy 2: Look for job cards with class names
                    if (jobElements.length === 0) {
                        jobElements = document.querySelectorAll('.job-card, [class*="job-card"], [class*="job-item"]');
                    }
                    
                    // Strategy 3: Look for h3 elements that might be job titles
                    if (jobElements.length === 0) {
                        const h3Elements = document.querySelectorAll('h3');
                        jobElements = Array.from(h3Elements).filter(h3 => {
                            const text = h3.textContent.toLowerCase();
                            return text.includes('software') || text.includes('developer') || text.includes('intern');
                        });
                    }
                    
                    // Strategy 4: Look for any elements with job-related text
                    if (jobElements.length === 0) {
                        const allElements = document.querySelectorAll('*');
                        jobElements = Array.from(allElements).filter(el => {
                            const text = el.textContent.toLowerCase();
                            return (text.includes('software developer') || text.includes('software engineering')) && 
                                   (text.includes('intern') || text.includes('summer'));
                        });
                    }
                    
                    console.log(`Found ${jobElements.length} potential job elements`);
                    
                    jobElements.forEach((card, index) => {
                        try {
                            // Extract job title - try multiple selectors
                            let titleElement = card.querySelector('h3, [data-testid="job-title"], .job-title, [class*="title"]');
                            if (!titleElement) {
                                titleElement = card;
                            }
                            const title = titleElement ? titleElement.textContent.trim() : '';
                            
                            // Extract company
                            let companyElement = card.querySelector('[data-testid="company-name"], .company-name, .job-company, [class*="company"]');
                            if (!companyElement) {
                                // Look for Google or other company names in the text
                                const companyText = card.textContent;
                                if (companyText.includes('Google')) {
                                    companyElement = { textContent: 'Google' };
                                } else if (companyText.includes('YouTube')) {
                                    companyElement = { textContent: 'YouTube' };
                                } else {
                                    companyElement = { textContent: 'Google' };
                                }
                            }
                            const company = companyElement ? companyElement.textContent.trim() : 'Google';
                            
                            // Extract location
                            let locationElement = card.querySelector('[data-testid="job-location"], .job-location, .location, [class*="location"]');
                            if (!locationElement) {
                                // Look for location patterns in text
                                const text = card.textContent;
                                const locationMatch = text.match(/([A-Z][a-z]+(?:\\s+[A-Z][a-z]+)*,?\\s*(?:ON|QC|CA|USA|United States|Canada))/);
                                if (locationMatch) {
                                    locationElement = { textContent: locationMatch[1] };
                                } else {
                                    locationElement = { textContent: 'Multiple Locations' };
                                }
                            }
                            const location = locationElement ? locationElement.textContent.trim() : 'Multiple Locations';
                            
                            // Extract job link
                            let linkElement = card.querySelector('a[href*="/jobs/"], a[href*="careers"], a[href*="google.com"]');
                            if (!linkElement) {
                                // Look for any link in the card
                                linkElement = card.querySelector('a[href]');
                            }
                            const jobUrl = linkElement ? linkElement.href : '';
                            
                            // Extract job ID from URL or create one
                            let jobId = '';
                            if (jobUrl) {
                                const match = jobUrl.match(/\\/jobs\\/([^\\/]+)/);
                                if (match) {
                                    jobId = match[1];
                                }
                            }
                            
                            // If no job ID found, create one from title and index
                            if (!jobId) {
                                const titleSlug = title.toLowerCase().replace(/[^a-z0-9]/g, '_').substring(0, 20);
                                jobId = `google_${titleSlug}_${index}`;
                            }
                            
                            // Only add if we have a meaningful title
                            if (title && title.length > 5 && (title.toLowerCase().includes('software') || title.toLowerCase().includes('developer'))) {
                                jobs.push({
                                    id: jobId,
                                    title: title,
                                    company: company,
                                    location: location,
                                    url: jobUrl || 'https://careers.google.com'
                                });
                            }
                        } catch (error) {
                            console.error('Error processing job card:', error);
                        }
                    });
                    
                    return jobs;
                }
            """)
            
            # Process the extracted data
            for job_info in job_data:
                try:
                    # Get job details
                    job_id = job_info.get("id", "")
                    title = job_info.get("title", "").strip()
                    company = job_info.get("company", "Google").strip()
                    location = job_info.get("location", "Multiple Locations").strip()
                    job_url = job_info.get("url", "")
                    
                    if not title or not job_url:
                        continue
                    
                    # Clean up the job ID
                    if not job_id.startswith("google_"):
                        job_id = f"google_{job_id}"
                    
                    job_dict = {
                        "id": job_id,
                        "company": company,
                        "title": title,
                        "team": "Software Engineering",  # Default team for software developer roles
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
    """Test the Google scraper."""
    scraper = GoogleScraper(
        employment_type="INTERN",
        target_level="INTERN_AND_APPRENTICE",
        search_query="Software Developer",
        locations=["Canada", "United States"]
    )
    jobs = await scraper.scrape()
    
    print(f"\nFound {len(jobs)} Google jobs:")
    for job in jobs:
        print(f"\n- {job['title']}")
        print(f"  Company: {job['company']}")
        print(f"  Location: {job['location']}")
        print(f"  URL: {job['url']}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

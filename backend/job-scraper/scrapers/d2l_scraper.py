"""
D2L Careers Scraper - Playwright Version

Scrapes co-op and internship positions from D2L's careers page using Playwright
to handle JavaScript-rendered content.
"""

import asyncio
from typing import List, Dict, Optional
from datetime import datetime
import logging
import re

from playwright.async_api import async_playwright, Page, Browser

logger = logging.getLogger(__name__)


class D2LScraper:
    """Scraper for D2L careers page using Playwright for JavaScript rendering"""
    
    COMPANY_NAME = "D2L"
    BASE_URL = "https://www.d2l.com/careers/jobs/?status=co-op-internship&"
    
    def __init__(self):
        """Initialize the D2L scraper"""
        logger.info(f"D2L Playwright scraper initialized for: {self.BASE_URL}")

    async def scrape(self) -> List[Dict[str, str]]:
        """
        Scrape D2L co-op and internship job postings using Playwright
        
        Returns:
            List of job dictionaries with keys: id, company, title, team, location, url, description, posted_date
        """
        jobs = []
        
        try:
            async with async_playwright() as p:
                # Launch Firefox browser (more stable in headless mode)
                logger.info("Launching Playwright Firefox browser...")
                browser = await p.firefox.launch(
                    headless=True,
                    args=[]
                )
                
                # Create a new page
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )
                page = await context.new_page()
                
                logger.info(f"Navigating to D2L careers page...")
                await page.goto(self.BASE_URL, wait_until='networkidle', timeout=60000)
                
                # Wait for job listings to load
                logger.info("Waiting for job listings to load...")
                try:
                    # Wait for job list to appear
                    await page.wait_for_selector('li[data-ph-at-id]', timeout=10000)
                except Exception as e:
                    logger.warning(f"Timeout waiting for job selector: {e}")
                    # Continue anyway, jobs might still be there
                
                # Give it a bit more time for all jobs to render
                await page.wait_for_timeout(2000)
                
                # Extract job data
                jobs = await self._extract_jobs_from_page(page)
                
                logger.info(f"Successfully scraped {len(jobs)} jobs from D2L")
                
                # Close browser
                await browser.close()
                
        except Exception as e:
            logger.error(f"Error while scraping D2L with Playwright: {e}", exc_info=True)
        
        return jobs
    
    async def _extract_jobs_from_page(self, page: Page) -> List[Dict[str, str]]:
        """Extract job data from the loaded page"""
        jobs = []
        
        try:
            # Get all job listing elements
            job_elements = await page.query_selector_all('li[data-ph-at-id]')
            
            if not job_elements:
                # Fallback: try other selectors
                logger.warning("No jobs found with data-ph-at-id, trying alternative selectors...")
                job_elements = await page.query_selector_all('article, div[class*="job"], li[class*="job"]')
            
            logger.info(f"Found {len(job_elements)} job elements")
            
            for element in job_elements:
                try:
                    # Extract job data using JavaScript
                    job_data = await page.evaluate('''(element) => {
                        // Find heading (h3, h4, or h5)
                        const heading = element.querySelector('h3, h4, h5');
                        if (!heading) return null;
                        
                        // Find link in heading
                        const link = heading.querySelector('a');
                        if (!link) return null;
                        
                        const title = link.textContent.trim();
                        const url = link.href;
                        
                        // Extract reference number
                        const refMatch = title.match(/Ref\\s*#\\s*(\\d+)/i);
                        const ref = refMatch ? refMatch[1] : null;
                        
                        // Clean title (remove ref number)
                        const cleanTitle = ref ? title.replace(refMatch[0], '').trim() : title;
                        
                        // Get full text content for parsing
                        const fullText = element.textContent;
                        
                        // Extract department/team
                        let department = null;
                        const departments = ['Product Development', 'Engineering', 'Marketing', 'Sales', 
                                           'Professional Services and Support', 'Information Technology',
                                           'UX Research & Design', 'Corporate Operations', 'H5P'];
                        
                        for (const dept of departments) {
                            if (fullText.includes(dept)) {
                                department = dept;
                                break;
                            }
                        }
                        
                        // Extract location
                        let location = 'Remote';
                        const locationMatch = fullText.match(/(?:Kitchener|Toronto|Vancouver|Winnipeg|Remote[^\\n]*)/);
                        if (locationMatch) {
                            location = locationMatch[0].trim();
                        }
                        
                        // Extract job type
                        let jobType = 'Co-op/Internship';
                        if (fullText.includes('Full-time')) jobType = 'Full-time';
                        else if (fullText.includes('New Graduate')) jobType = 'New Graduate';
                        else if (fullText.includes('Part-time') || fullText.includes('Part time')) jobType = 'Part-time';
                        
                        // Extract posted date
                        let postedDate = null;
                        const dateMatch = fullText.match(/Posted Date:\\s*(\\d{1,2}\\/\\d{1,2}\\/\\d{4})/);
                        if (dateMatch) {
                            postedDate = dateMatch[1];
                        }
                        
                        // Extract description
                        const descPara = element.querySelector('p');
                        const description = descPara ? descPara.textContent.trim() : null;
                        
                        return {
                            ref: ref,
                            title: cleanTitle,
                            url: url,
                            department: department,
                            location: location,
                            jobType: jobType,
                            postedDate: postedDate,
                            description: description
                        };
                    }''', element)
                    
                    if not job_data or not job_data.get('ref'):
                        continue
                    
                    # Parse posted date
                    posted_date = datetime.utcnow()
                    if job_data.get('postedDate'):
                        try:
                            posted_date = datetime.strptime(job_data['postedDate'], "%m/%d/%Y")
                        except Exception as e:
                            logger.warning(f"Could not parse date '{job_data['postedDate']}': {e}")
                    
                    # Create job dictionary
                    job = {
                        "id": f"d2l_{job_data['ref']}",
                        "company": self.COMPANY_NAME,
                        "title": job_data['title'],
                        "team": job_data.get('department') or 'Co-op/Internship',
                        "location": job_data.get('location') or 'Kitchener, Ontario',
                        "url": job_data['url'],
                        "description": job_data.get('description'),
                        "posted_date": posted_date,
                    }
                    
                    jobs.append(job)
                    logger.debug(f"Scraped job: {job['title']} ({job['location']})")
                    
                except Exception as e:
                    logger.error(f"Error extracting job data: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error extracting jobs from page: {e}", exc_info=True)
        
        return jobs


# Convenience function for the scheduler
async def scrape_d2l() -> List[Dict[str, str]]:
    """
    Convenience function to scrape D2L co-op and internship jobs using Playwright
    
    Returns:
        List of job dictionaries
    """
    scraper = D2LScraper()
    return await scraper.scrape()

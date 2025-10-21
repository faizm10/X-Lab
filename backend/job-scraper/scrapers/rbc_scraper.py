"""
RBC Careers Scraper

Scrapes job postings from RBC's student and early talent careers page.
"""

import asyncio
from typing import List, Dict, Optional
from datetime import datetime
import logging
import re

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class RBCScraper:
    """Scraper for RBC careers page"""
    
    COMPANY_NAME = "RBC"
    BASE_URL = "https://jobs.rbc.com/ca/en/featuredopportunities/student-early-talent-jobs"
    
    def __init__(self):
        """Initialize the RBC scraper"""
        logger.info(f"RBC scraper initialized for: {self.BASE_URL}")

    async def scrape(self) -> List[Dict[str, str]]:
        """
        Scrape RBC job postings for students and early talent
        
        Returns:
            List of job dictionaries with keys: id, company, title, team, location, url, description, posted_date
        """
        jobs = []
        
        try:
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                logger.info(f"Fetching RBC careers page: {self.BASE_URL}")
                
                # Fetch the careers page
                response = await client.get(self.BASE_URL)
                response.raise_for_status()
                
                # Parse the HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find all job listings - they are in <li> elements within the jobs list
                job_list_items = soup.find_all('li', {'role': 'listitem'})
                
                logger.info(f"Found {len(job_list_items)} job listings")
                
                for item in job_list_items:
                    try:
                        # Find the h3 heading with the job title link
                        heading = item.find('h3')
                        if not heading:
                            continue
                        
                        link = heading.find('a', href=True)
                        if not link:
                            continue
                        
                        # Extract job URL and title
                        job_url = link.get('href', '')
                        if not job_url.startswith('http'):
                            job_url = f"https://jobs.rbc.com{job_url}"
                        
                        title = link.get_text(strip=True)
                        
                        # Extract job ID from URL
                        # URL format: https://jobs.rbc.com/ca/en/job/R-0000143096/Financial-Solutions-Intern
                        job_id = None
                        if '/job/' in job_url:
                            parts = job_url.split('/job/')[1].split('/')
                            if parts:
                                job_id = parts[0]
                        
                        if not job_id:
                            logger.warning(f"Could not extract job ID from URL: {job_url}")
                            continue
                        
                        # Find the paragraph containing job details
                        details_para = item.find('p')
                        
                        category = None
                        location = None
                        job_type = None
                        posted_date_str = None
                        
                        if details_para:
                            # Extract all detail spans
                            detail_spans = details_para.find_all('span')
                            
                            for i, span in enumerate(detail_spans):
                                text = span.get_text(strip=True)
                                
                                # The pattern is: Label, Empty span, Value
                                if text == 'Category' and i + 2 < len(detail_spans):
                                    category = detail_spans[i + 2].get_text(strip=True)
                                elif text == 'Location' and i + 2 < len(detail_spans):
                                    location = detail_spans[i + 2].get_text(strip=True)
                                elif text == 'Job Type' and i + 2 < len(detail_spans):
                                    job_type = detail_spans[i + 2].get_text(strip=True)
                                elif 'Posted Date:' in text:
                                    posted_date_str = text.replace('Posted Date:', '').strip()
                        
                        # Parse posted date
                        posted_date = datetime.utcnow()  # Default to now
                        if posted_date_str:
                            try:
                                # Format: "10/15/2025"
                                posted_date = datetime.strptime(posted_date_str, "%m/%d/%Y")
                            except Exception as e:
                                logger.warning(f"Could not parse date '{posted_date_str}': {e}")
                        
                        # Set team from category if available
                        team = category if category else "Student & Early Talent"
                        
                        # Create job dictionary
                        job = {
                            "id": f"rbc_{job_id}",
                            "company": self.COMPANY_NAME,
                            "title": title,
                            "team": team,
                            "location": location or "Not specified",
                            "url": job_url,
                            "description": f"{team} - {job_type or 'Position'} in {location or 'Various locations'}",
                            "posted_date": posted_date,
                        }
                        
                        jobs.append(job)
                        logger.debug(f"Scraped job: {title} ({location})")
                        
                    except Exception as e:
                        logger.error(f"Error parsing job item: {e}", exc_info=True)
                        continue
                
                logger.info(f"Successfully scraped {len(jobs)} jobs from RBC")
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error while scraping RBC: {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"Request error while scraping RBC: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while scraping RBC: {e}", exc_info=True)
        
        return jobs


# Convenience function for the scheduler
async def scrape_rbc() -> List[Dict[str, str]]:
    """
    Convenience function to scrape RBC jobs
    
    Returns:
        List of job dictionaries
    """
    scraper = RBCScraper()
    return await scraper.scrape()


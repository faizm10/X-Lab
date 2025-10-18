"""
Microsoft Careers Scraper
Scrapes job listings from Microsoft's career API
"""
import asyncio
from typing import List, Dict, Optional
import httpx
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class MicrosoftScraper:
    """Scraper for Microsoft careers API"""
    
    BASE_URL = "https://gcsservices.careers.microsoft.com/search/api/v1/search"
    COMPANY_NAME = "Microsoft"
    
    def __init__(
        self, 
        professions: Optional[List[str]] = None,
        experience: Optional[str] = None,
        employment_type: Optional[str] = None,
        location: Optional[str] = None
    ):
        """
        Initialize the Microsoft scraper
        
        Args:
            professions: Filter by profession(s) (e.g., ["Engineering", "Software Engineering"])
            experience: Filter by experience level (e.g., "Students and graduates")
            employment_type: Filter by type (e.g., "Internship", "Full-Time")
            location: Filter by location (e.g., "Redmond, Washington")
        """
        self.professions = professions or ["Engineering", "Software Engineering"]
        self.experience = experience or "Students and graduates"
        self.employment_type = employment_type or "Internship"
        self.location = location
        
    def _build_params(self, page: int = 1) -> Dict[str, str]:
        """Build the API query parameters"""
        params = {
            "l": "en_us",
            "pg": str(page),
            "pgSz": "20",
            "o": "Recent",  # Sort by most recent
            "flt": "true",
        }
        
        # Add professions (can be multiple)
        if self.professions:
            for profession in self.professions:
                # For multiple values with same key, we need to handle this specially
                # The API accepts multiple 'p' parameters
                if "p" not in params:
                    params["p"] = profession
        
        if self.experience:
            params["exp"] = self.experience
            
        if self.employment_type:
            params["et"] = self.employment_type
            
        if self.location:
            params["loc"] = self.location
        
        return params
    
    def _build_url_with_multiple_professions(self, page: int = 1) -> str:
        """Build URL manually to handle multiple profession parameters"""
        params = []
        
        # Add professions first (multiple p= parameters)
        if self.professions:
            for profession in self.professions:
                params.append(f"p={profession.replace(' ', '%20')}")
        
        if self.experience:
            params.append(f"exp={self.experience.replace(' ', '%20')}")
            
        if self.employment_type:
            params.append(f"et={self.employment_type.replace(' ', '%20')}")
            
        if self.location:
            params.append(f"loc={self.location.replace(' ', '%20')}")
        
        # Add pagination and filters
        params.extend([
            "l=en_us",
            f"pg={page}",
            "pgSz=20",
            "o=Recent",
            "flt=true"
        ])
        
        return f"{self.BASE_URL}?{'&'.join(params)}"
    
    async def scrape(self) -> List[Dict[str, str]]:
        """
        Scrape all job postings from Microsoft careers API
        
        Returns:
            List of job dictionaries with keys: id, company, title, team, location, url
        """
        jobs = []
        
        try:
            async with httpx.AsyncClient(
                timeout=30.0,
                follow_redirects=True,
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "application/json",
                }
            ) as client:
                # Scrape first page
                url = self._build_url_with_multiple_professions(1)
                logger.info(f"Scraping Microsoft careers API: {url}")
                response = await client.get(url)
                response.raise_for_status()
                
                data = response.json()
                
                # Extract jobs from first page
                page_jobs = self._extract_jobs_from_response(data)
                jobs.extend(page_jobs)
                logger.info(f"Scraped {len(page_jobs)} jobs from page 1")
                
                # Check if there are more pages
                total_jobs = data.get("operationResult", {}).get("result", {}).get("totalJobs", 0)
                page_size = 20
                total_pages = (total_jobs + page_size - 1) // page_size
                
                logger.info(f"Found {total_jobs} total jobs across {total_pages} page(s)")
                
                # Scrape remaining pages
                for page_num in range(2, total_pages + 1):
                    await asyncio.sleep(0.5)  # Be respectful
                    
                    url = self._build_url_with_multiple_professions(page_num)
                    logger.info(f"Scraping page {page_num}...")
                    response = await client.get(url)
                    response.raise_for_status()
                    
                    data = response.json()
                    page_jobs = self._extract_jobs_from_response(data)
                    jobs.extend(page_jobs)
                    logger.info(f"Scraped {len(page_jobs)} jobs from page {page_num}")
                
        except Exception as e:
            logger.error(f"Error scraping Microsoft: {e}")
            raise
        
        logger.info(f"Total jobs scraped from Microsoft: {len(jobs)}")
        return jobs
    
    def _extract_jobs_from_response(self, data: Dict) -> List[Dict[str, str]]:
        """Extract all jobs from the API response"""
        jobs = []
        
        try:
            # Navigate to the jobs array in the response
            operation_result = data.get("operationResult", {})
            result = operation_result.get("result", {})
            job_list = result.get("jobs", [])
            
            for job_data in job_list:
                try:
                    # Extract job ID
                    job_id = job_data.get("jobId")
                    if not job_id:
                        logger.warning("Job missing ID, skipping")
                        continue
                    
                    # Get job title
                    title = job_data.get("title", "Unknown Title")
                    
                    # Get posting date and parse it
                    posted_date = None
                    posted_date_str = job_data.get("postingDate")
                    if posted_date_str:
                        try:
                            # Microsoft API returns dates in ISO format (e.g., "2024-10-15T00:00:00Z")
                            posted_date = datetime.fromisoformat(posted_date_str.replace('Z', '+00:00'))
                        except Exception as e:
                            logger.warning(f"Could not parse posting date '{posted_date_str}': {e}")
                    
                    # Get location (primary location)
                    location = None
                    properties = job_data.get("properties", {})
                    primary_location = properties.get("primaryLocation")
                    if primary_location:
                        location = primary_location
                    
                    # Get team/profession
                    team = None
                    profession = properties.get("profession")
                    if profession:
                        team = profession
                    
                    # Get work site (remote/hybrid/onsite)
                    work_site = properties.get("workSiteFlexibility")
                    if work_site and location:
                        location = f"{location} ({work_site})"
                    
                    # Build job URL
                    job_url = f"https://jobs.careers.microsoft.com/global/en/job/{job_id}"
                    
                    # Create unique ID with company prefix
                    unique_id = f"microsoft_{job_id}"
                    
                    job = {
                        "id": unique_id,
                        "company": self.COMPANY_NAME,
                        "title": title,
                        "team": team,
                        "location": location,
                        "url": job_url,
                        "description": None,  # Would need to fetch individual job page
                        "posted_date": posted_date
                    }
                    
                    jobs.append(job)
                    logger.debug(f"Extracted job: {title} ({unique_id})")
                    
                except Exception as e:
                    logger.error(f"Error extracting job data: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error parsing API response: {e}")
        
        return jobs


# Convenience function for the scheduler
async def scrape_microsoft(
    professions: Optional[List[str]] = None,
    experience: Optional[str] = "Students and graduates",
    employment_type: Optional[str] = "Internship",
    location: Optional[str] = None
) -> List[Dict[str, str]]:
    """
    Convenience function to scrape Microsoft jobs
    
    Args:
        professions: Filter by profession(s) (default: ["Engineering", "Software Engineering"])
        experience: Filter by experience level (default: "Students and graduates")
        employment_type: Filter by employment type (default: "Internship")
        location: Filter by location (optional)
        
    Returns:
        List of job dictionaries
    """
    if professions is None:
        professions = ["Engineering", "Software Engineering"]
    
    scraper = MicrosoftScraper(
        professions=professions,
        experience=experience,
        employment_type=employment_type,
        location=location
    )
    return await scraper.scrape()


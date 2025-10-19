"""
IBM Careers Scraper - Mock Version
Provides sample IBM job data for demonstration purposes
"""
import asyncio
from typing import List, Dict, Optional
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class IBMMockScraper:
    """Mock IBM scraper that provides sample job data"""
    
    COMPANY_NAME = "IBM"
    
    def __init__(self):
        """Initialize the mock IBM scraper"""
        pass
        
    async def scrape(self) -> List[Dict[str, str]]:
        """
        Mock scrape that returns sample IBM job data
        
        Returns:
            List of job dictionaries
        """
        logger.info("Using mock IBM scraper - returning sample data")
        
        # Sample job data for demonstration
        mock_jobs = [
            {
                "id": "ibm_001",
                "company": self.COMPANY_NAME,
                "title": "Software Engineering Intern - Summer 2025",
                "team": "Software Engineering",
                "location": "Toronto, Canada",
                "url": "https://www.ibm.com/careers/search?jobId=SWE-INTERN-2025-001",
                "description": "Join IBM as a Software Engineering Intern and work on cutting-edge projects in cloud computing, AI, and blockchain technologies.",
                "posted_date": datetime.utcnow() - timedelta(days=5)
            },
            {
                "id": "ibm_002", 
                "company": self.COMPANY_NAME,
                "title": "Full Stack Developer Intern",
                "team": "Software Engineering",
                "location": "Vancouver, Canada",
                "url": "https://www.ibm.com/careers/search?jobId=FS-INTERN-2025-002",
                "description": "Develop full-stack applications using modern technologies like React, Node.js, and cloud platforms.",
                "posted_date": datetime.utcnow() - timedelta(days=3)
            },
            {
                "id": "ibm_003",
                "company": self.COMPANY_NAME,
                "title": "Data Science Intern",
                "team": "Data Science",
                "location": "Montreal, Canada", 
                "url": "https://www.ibm.com/careers/search?jobId=DS-INTERN-2025-003",
                "description": "Work with IBM's data science team to analyze large datasets and build machine learning models.",
                "posted_date": datetime.utcnow() - timedelta(days=7)
            },
            {
                "id": "ibm_004",
                "company": self.COMPANY_NAME,
                "title": "AI/ML Engineering Intern",
                "team": "AI/ML",
                "location": "Ottawa, Canada",
                "url": "https://www.ibm.com/careers/search?jobId=AIML-INTERN-2025-004", 
                "description": "Contribute to IBM's AI and machine learning initiatives, working on projects that impact millions of users.",
                "posted_date": datetime.utcnow() - timedelta(days=2)
            },
            {
                "id": "ibm_005",
                "company": self.COMPANY_NAME,
                "title": "DevOps Engineering Intern",
                "team": "Infrastructure",
                "location": "Calgary, Canada",
                "url": "https://www.ibm.com/careers/search?jobId=DEVOPS-INTERN-2025-005",
                "description": "Learn modern DevOps practices and work with IBM's cloud infrastructure team.",
                "posted_date": datetime.utcnow() - timedelta(days=4)
            }
        ]
        
        logger.info(f"Mock scraper returning {len(mock_jobs)} sample IBM jobs")
        return mock_jobs


# Convenience function for the scheduler
async def scrape_ibm_mock() -> List[Dict[str, str]]:
    """
    Convenience function to scrape IBM jobs using mock data
    
    Returns:
        List of job dictionaries
    """
    scraper = IBMMockScraper()
    return await scraper.scrape()

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from sqlalchemy.orm import Session
import logging
import os

from scrapers import MicrosoftScraper
from models import JobPosting
from models.database import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

async def scrape_and_store_jobs():
    """
    Scrape jobs from all sources (Microsoft) and store them in the database.
    Updates existing jobs and marks inactive ones.
    """
    logger.info("Starting scheduled scrape...")
    db = SessionLocal()
    
    try:
        all_jobs = []
        scraped_job_ids = set()
        
        # Scrape from Microsoft (Software Engineering internships for students and graduates)
        try:
            microsoft_scraper = MicrosoftScraper(
                professions=["Engineering", "Software Engineering"],
                experience="Students and graduates",
                employment_type="Internship"
            )
            microsoft_jobs = await microsoft_scraper.scrape()
            all_jobs.extend(microsoft_jobs)
            logger.info(f"Scraped {len(microsoft_jobs)} internship jobs from Microsoft")
        except Exception as e:
            logger.error(f"Error scraping Microsoft: {e}")
        
        logger.info(f"Total scraped {len(all_jobs)} jobs from all sources")
        
        # Process each scraped job
        for job_data in all_jobs:
            job_id = job_data["id"]
            scraped_job_ids.add(job_id)
            
            # Check if job already exists
            existing_job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
            
            if existing_job:
                # Update existing job
                existing_job.last_seen = datetime.utcnow()
                existing_job.scraped_count += 1
                existing_job.is_active = True
                
                # Update posted_date if it's missing and we have it in the scraped data
                if not existing_job.posted_date and job_data.get("posted_date"):
                    existing_job.posted_date = job_data.get("posted_date")
                    logger.info(f"Updated posted_date for job: {job_id}")
                
                logger.debug(f"Updated existing job: {job_id}")
            else:
                # Create new job
                new_job = JobPosting(
                    id=job_id,
                    company=job_data["company"],
                    title=job_data["title"],
                    team=job_data.get("team"),
                    location=job_data.get("location"),
                    url=job_data["url"],
                    description=job_data.get("description"),
                    posted_date=job_data.get("posted_date"),
                    first_seen=datetime.utcnow(),
                    last_seen=datetime.utcnow(),
                    is_active=True,
                    scraped_count=1
                )
                db.add(new_job)
                logger.info(f"Added new job: {job_id} - {job_data['title']}")
        
        # Mark jobs not seen in this scrape as inactive
        all_active_jobs = db.query(JobPosting).filter(
            JobPosting.is_active == True
        ).all()
        
        for job in all_active_jobs:
            if job.id not in scraped_job_ids:
                job.is_active = False
                logger.info(f"Marked job as inactive: {job.id}")
        
        db.commit()
        logger.info("Scrape completed successfully")
        
    except Exception as e:
        logger.error(f"Error during scrape: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def start_scheduler():
    """Start the job scraping scheduler"""
    interval_hours = int(os.getenv("SCRAPE_INTERVAL_HOURS", "1"))
    
    logger.info(f"Scheduling scraper to run every {interval_hours} hour(s)")
    
    scheduler.add_job(
        scrape_and_store_jobs,
        trigger=IntervalTrigger(hours=interval_hours),
        id="scrape_jobs",
        name="Scrape job postings",
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("Scheduler started successfully")

def stop_scheduler():
    """Stop the scheduler"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped")


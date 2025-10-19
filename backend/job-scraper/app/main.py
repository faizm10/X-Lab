from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
import os
import logging

from models import JobPosting
from models.database import get_db, init_db
from app.scheduler import start_scheduler, scrape_and_store_jobs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Job Scraper API",
    description="API for scraping and tracking job postings",
    version="1.0.0"
)

# CORS middleware
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize database and start scheduler on startup"""
    logger.info("Starting up Job Scraper API...")
    init_db()
    logger.info("Database initialized")
    
    # Run initial scrape
    logger.info("Running initial scrape...")
    await scrape_and_store_jobs()
    
    # Start scheduler
    start_scheduler()
    logger.info("Scheduler started")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Job Scraper API",
        "version": "1.0.0",
        "endpoints": {
            "jobs": "/api/jobs",
            "stats": "/api/stats",
            "scrape": "/api/scrape"
        },
        "companies_tracked": ["Pinterest", "Microsoft", "IBM"],
        "scraping_frequency": "Every hour"
    }

@app.get("/api/jobs")
async def get_jobs(
    company: Optional[str] = Query(None, description="Filter by company"),
    active_only: bool = Query(True, description="Only return active jobs"),
    keywords: Optional[str] = Query(None, description="Filter by keywords (comma-separated, e.g., 'intern,internship,co-op')"),
    limit: int = Query(100, ge=1, le=500, description="Number of jobs to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: Session = Depends(get_db)
):
    """Get job postings with optional filtering"""
    query = db.query(JobPosting)
    
    if company:
        query = query.filter(JobPosting.company == company)
    
    if active_only:
        query = query.filter(JobPosting.is_active == True)
    
    # Order by first_seen descending (newest first)
    query = query.order_by(JobPosting.first_seen.desc())
    
    # Get all jobs first
    all_jobs = query.all()
    
    # Keyword filtering - case insensitive exact word match in title (post-query)
    if keywords:
        import re
        keyword_list = [kw.strip().lower() for kw in keywords.split(',')]
        
        filtered_jobs = []
        for job in all_jobs:
            job_title_lower = job.title.lower()
            # Check if any keyword matches as a whole word
            for keyword in keyword_list:
                # Use regex with word boundaries to match exact words
                # \b matches word boundaries, so "intern" won't match "internal"
                pattern = rf'\b{re.escape(keyword)}\b'
                if re.search(pattern, job_title_lower):
                    filtered_jobs.append(job)
                    break  # Found a match, no need to check other keywords
        
        all_jobs = filtered_jobs
    
    # Apply pagination after filtering
    total = len(all_jobs)
    jobs = all_jobs[offset:offset + limit]
    
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "jobs": [job.to_dict() for job in jobs]
    }

@app.get("/api/jobs/{job_id}")
async def get_job(job_id: str, db: Session = Depends(get_db)):
    """Get a specific job by ID"""
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job.to_dict()

@app.get("/api/jobs/new/today")
async def get_new_jobs_today(
    company: Optional[str] = Query(None, description="Filter by company"),
    db: Session = Depends(get_db)
):
    """Get jobs first seen today"""
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    query = db.query(JobPosting).filter(
        JobPosting.first_seen >= today_start,
        JobPosting.is_active == True
    )
    
    if company:
        query = query.filter(JobPosting.company == company)
    
    jobs = query.order_by(JobPosting.first_seen.desc()).all()
    
    return {
        "date": today_start.isoformat(),
        "count": len(jobs),
        "jobs": [job.to_dict() for job in jobs]
    }

@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get statistics about job postings"""
    total_jobs = db.query(JobPosting).count()
    active_jobs = db.query(JobPosting).filter(JobPosting.is_active == True).count()
    
    # Jobs added today
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    new_today = db.query(JobPosting).filter(
        JobPosting.first_seen >= today_start
    ).count()
    
    # Jobs added in last 7 days
    week_ago = datetime.utcnow() - timedelta(days=7)
    new_this_week = db.query(JobPosting).filter(
        JobPosting.first_seen >= week_ago
    ).count()
    
    # Get companies
    companies = db.query(JobPosting.company).distinct().all()
    companies = [c[0] for c in companies]
    
    # Last scrape time (most recent last_seen)
    last_job = db.query(JobPosting).order_by(JobPosting.last_seen.desc()).first()
    last_scraped = last_job.last_seen if last_job else None
    
    return {
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "new_today": new_today,
        "new_this_week": new_this_week,
        "companies_tracked": len(companies),
        "companies": companies,
        "last_scraped": last_scraped.isoformat() if last_scraped else None
    }

@app.post("/api/scrape")
async def trigger_scrape(
    company: str = Query("stripe", description="Company to scrape"),
    db: Session = Depends(get_db)
):
    """Manually trigger a scrape"""
    logger.info(f"Manual scrape triggered for: {company}")
    
    try:
        await scrape_and_store_jobs()
        
        return {
            "status": "success",
            "message": f"Scrape completed for {company}",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error during manual scrape: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


#!/usr/bin/env python3
"""
Script to clean/reset the job database.
Deletes all job postings from the database.
"""
import sys
import os
import logging
from sqlalchemy.orm import Session

# Add parent directory to path to import models
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.database import SessionLocal, engine
from models.job import JobPosting, Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_database():
    """Delete all jobs from the database"""
    db: Session = SessionLocal()
    
    try:
        # Count current jobs
        total_jobs = db.query(JobPosting).count()
        logger.info(f"Found {total_jobs} jobs in database")
        
        if total_jobs == 0:
            logger.info("Database is already empty. Nothing to clean.")
            return
        
        # Delete all jobs
        deleted_count = db.query(JobPosting).delete()
        db.commit()
        
        logger.info(f"✅ Successfully deleted {deleted_count} jobs from database")
        logger.info("Database is now clean and ready for fresh job data")
        
    except Exception as e:
        logger.error(f"❌ Error cleaning database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def reset_database():
    """Drop all tables and recreate them (nuclear option)"""
    try:
        logger.info("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        
        logger.info("Creating fresh tables...")
        Base.metadata.create_all(bind=engine)
        
        logger.info("✅ Database has been completely reset")
        logger.info("All tables have been dropped and recreated")
        
    except Exception as e:
        logger.error(f"❌ Error resetting database: {e}")
        raise

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Clean or reset the job database")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Drop and recreate all tables (nuclear option - deletes everything including schema)"
    )
    
    args = parser.parse_args()
    
    if args.reset:
        logger.warning("⚠️  WARNING: This will drop all tables and recreate them!")
        response = input("Are you sure you want to reset the database? (yes/no): ")
        if response.lower() == "yes":
            reset_database()
        else:
            logger.info("Reset cancelled")
    else:
        clean_database()


#!/usr/bin/env python3
"""
Test script for BMO scraper
"""
import asyncio
import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.bmo_scraper import BMOScraper

async def test_bmo_scraper():
    """Test the BMO scraper"""
    print("🏦 Testing BMO Scraper...")
    
    try:
        # Create BMO scraper
        bmo_scraper = BMOScraper(
            keywords=["intern", "internship", "co-op", "coop"],
            location=None,
            job_type="Internship"
        )
        
        print("📡 Scraping BMO careers...")
        jobs = await bmo_scraper.scrape()
        
        print(f"✅ Found {len(jobs)} BMO jobs")
        
        if jobs:
            print("\n📋 Sample jobs:")
            for i, job in enumerate(jobs[:3]):  # Show first 3 jobs
                print(f"  {i+1}. {job['title']}")
                print(f"     Company: {job['company']}")
                print(f"     Location: {job.get('location', 'N/A')}")
                print(f"     URL: {job['url']}")
                print()
        else:
            print("ℹ️  No jobs found (this might be normal if no intern positions are currently posted)")
            
    except Exception as e:
        print(f"❌ Error testing BMO scraper: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_bmo_scraper())

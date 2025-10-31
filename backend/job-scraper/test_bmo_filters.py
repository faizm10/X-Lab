#!/usr/bin/env python3
"""
Test script for BMO scraper with filters
"""
import asyncio
import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.bmo_scraper import BMOScraper

async def test_bmo_with_filters():
    """Test the BMO scraper with filters"""
    print("🏦 Testing BMO Scraper with Filters...")
    
    try:
        # Create BMO scraper with filters
        bmo_scraper = BMOScraper(
            keywords=["intern", "internship", "co-op", "coop"],
            location="Ontario",  # Explicitly set Ontario
            job_type="Intern (Fixed Term)"
        )
        
        print("📡 Scraping BMO careers with filters...")
        print("🔍 Filters: Ontario, Technology, Intern (Fixed Term)")
        
        jobs = await bmo_scraper.scrape()
        
        print(f"✅ Found {len(jobs)} BMO jobs")
        
        if jobs:
            print("\n📋 All jobs found:")
            for i, job in enumerate(jobs):
                print(f"  {i+1}. {job['title']}")
                print(f"     Company: {job['company']}")
                print(f"     Location: {job.get('location', 'N/A')}")
                print(f"     Team: {job.get('team', 'N/A')}")
                print(f"     URL: {job['url']}")
                print()
        else:
            print("ℹ️  No jobs found - this might indicate:")
            print("   - BMO website structure has changed")
            print("   - No intern positions currently posted")
            print("   - Selectors need adjustment")
            print("   - URL parameters need refinement")
            
    except Exception as e:
        print(f"❌ Error testing BMO scraper: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_bmo_with_filters())

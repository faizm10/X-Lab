#!/usr/bin/env python3
"""Quick test script to check if bank scrapers are returning jobs"""
import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scrapers.rbc_scraper import RBCScraper
from scrapers.bmo_scraper import BMOScraper
from scrapers.cibc_scraper import CIBCScraper
from scrapers.interac_scraper import InteracScraper

async def test_scraper(scraper, name):
    """Test a scraper and report results"""
    try:
        print(f"\n{'='*60}")
        print(f"Testing {name} scraper...")
        print(f"{'='*60}")
        jobs = await scraper.scrape()
        print(f"✅ {name}: Found {len(jobs)} jobs")
        if jobs:
            print(f"Sample job: {jobs[0].get('title', 'N/A')}")
        return len(jobs)
    except Exception as e:
        print(f"❌ {name}: Error - {e}")
        import traceback
        traceback.print_exc()
        return 0

async def main():
    """Test all bank scrapers"""
    print("Testing Big Bank Scrapers")
    print("="*60)
    
    results = {}
    
    # Test RBC
    rbc_scraper = RBCScraper(
        keywords=["intern", "internship", "co-op", "coop"],
        location=None,
        job_type="Internship"
    )
    results['RBC'] = await test_scraper(rbc_scraper, "RBC")
    
    # Test BMO
    bmo_scraper = BMOScraper(
        keywords=["intern", "internship", "co-op", "coop"],
        location=None,
        job_type="Internship"
    )
    results['BMO'] = await test_scraper(bmo_scraper, "BMO")
    
    # Test CIBC
    cibc_scraper = CIBCScraper(
        keywords=["intern", "internship", "co-op", "coop"],
        location=None,
        job_type="Internship"
    )
    results['CIBC'] = await test_scraper(cibc_scraper, "CIBC")
    
    # Test Interac
    interac_scraper = InteracScraper(
        keywords=["intern", "internship", "co-op", "coop"],
        location=None,
        job_type="Internship"
    )
    results['Interac'] = await test_scraper(interac_scraper, "Interac")
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for bank, count in results.items():
        status = "✅" if count > 0 else "❌"
        print(f"{status} {bank}: {count} jobs")
    
    total = sum(results.values())
    print(f"\nTotal jobs found: {total}")

if __name__ == "__main__":
    asyncio.run(main())


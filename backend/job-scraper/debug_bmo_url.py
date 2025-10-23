#!/usr/bin/env python3
"""
Debug BMO URL structure
"""
import asyncio
import httpx
import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def debug_bmo_urls():
    """Debug BMO URL structure"""
    print("🔍 Debugging BMO URL Structure...")
    
    # Try different BMO URLs
    urls_to_try = [
        "https://jobs.bmo.com/global/en/home",
        "https://jobs.bmo.com/global/en/search-results",
        "https://jobs.bmo.com/global/en/search-results?keywords=intern&location=Ontario",
        "https://jobs.bmo.com/global/en/search-results?keywords=intern&location=Ontario&department=Technology",
        "https://jobs.bmo.com/global/en/search-results?keywords=intern&location=Ontario&department=Technology&jobType=Intern%20(Fixed%20Term)"
    ]
    
    async with httpx.AsyncClient(
        timeout=30.0,
        follow_redirects=True,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
    ) as client:
        
        for i, url in enumerate(urls_to_try, 1):
            print(f"\n{i}. Testing URL: {url}")
            try:
                response = await client.get(url)
                print(f"   Status: {response.status_code}")
                print(f"   Content Length: {len(response.text)}")
                
                # Look for job-related content
                if "job" in response.text.lower() or "intern" in response.text.lower():
                    print("   ✅ Found job-related content")
                else:
                    print("   ❌ No job-related content found")
                    
                # Look for specific selectors
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Check for common job selectors
                job_selectors = [
                    'div[data-automation-id="jobTitle"]',
                    '.job-title',
                    '.job-listing',
                    '.search-result',
                    'article',
                    '.job-item',
                    '[data-testid="job-card"]',
                    '.job-card',
                    '.search-result-item'
                ]
                
                found_selectors = []
                for selector in job_selectors:
                    elements = soup.select(selector)
                    if elements:
                        found_selectors.append(f"{selector} ({len(elements)} elements)")
                
                if found_selectors:
                    print(f"   ✅ Found selectors: {', '.join(found_selectors)}")
                else:
                    print("   ❌ No job selectors found")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(debug_bmo_urls())

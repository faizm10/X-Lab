#!/usr/bin/env python3
"""
Find BMO selectors by analyzing the HTML structure
"""
import asyncio
import httpx
import sys
import os
import re

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def find_bmo_selectors():
    """Find the actual BMO selectors"""
    print("🔍 Finding BMO Selectors...")
    
    url = "https://jobs.bmo.com/global/en/search-results?keywords=intern&location=Ontario&department=Technology&jobType=Intern%20(Fixed%20Term)"
    
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
        
        print(f"📡 Fetching: {url}")
        response = await client.get(url)
        print(f"✅ Status: {response.status_code}")
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        print(f"📄 Content Length: {len(response.text)}")
        
        # Look for any elements that might contain job information
        print("\n🔍 Searching for job-related elements...")
        
        # Look for elements with job-related text
        job_keywords = ['intern', 'job', 'position', 'career', 'title', 'location']
        
        for keyword in job_keywords:
            elements = soup.find_all(text=re.compile(keyword, re.IGNORECASE))
            if elements:
                print(f"   Found '{keyword}' in {len(elements)} text elements")
                # Show first few examples
                for i, elem in enumerate(elements[:3]):
                    parent = elem.parent
                    if parent:
                        print(f"     {i+1}. {parent.name} with class='{parent.get('class', [])}'")
        
        # Look for common job listing patterns
        print("\n🔍 Looking for common job listing patterns...")
        
        # Check for divs with job-related classes
        job_divs = soup.find_all('div', class_=re.compile(r'job|listing|result|card|item', re.IGNORECASE))
        print(f"   Found {len(job_divs)} divs with job-related classes")
        
        # Check for articles
        articles = soup.find_all('article')
        print(f"   Found {len(articles)} article elements")
        
        # Check for links that might be job titles
        job_links = soup.find_all('a', href=re.compile(r'job|career', re.IGNORECASE))
        print(f"   Found {len(job_links)} links with job/career in href")
        
        # Look for specific BMO patterns
        print("\n🔍 Looking for BMO-specific patterns...")
        
        # Check for Workday patterns (BMO might use Workday)
        workday_elements = soup.find_all(attrs={'data-automation-id': True})
        print(f"   Found {len(workday_elements)} elements with data-automation-id")
        
        if workday_elements:
            automation_ids = [elem.get('data-automation-id') for elem in workday_elements[:10]]
            print(f"   Sample automation IDs: {automation_ids}")
        
        # Look for any elements with job-related attributes
        job_attrs = soup.find_all(attrs={'data-job': True}) + soup.find_all(attrs={'data-position': True})
        print(f"   Found {len(job_attrs)} elements with job/position attributes")
        
        # Save a sample of the HTML for manual inspection
        print("\n💾 Saving sample HTML for manual inspection...")
        with open('bmo_sample.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("   Saved to bmo_sample.html")

if __name__ == "__main__":
    asyncio.run(find_bmo_selectors())

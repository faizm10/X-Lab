# Job Scrapers

This directory contains scrapers for various company job boards.

## Currently Active Scrapers

The following scrapers are currently scheduled in `app/scheduler.py`:
- **Microsoft** - Engineering internships (via official API)
- **RBC** - Intern/Co-op positions
- **BMO** - Intern/Co-op positions
- **CIBC** - Intern/Co-op positions
- **Interac** - Intern/Co-op positions
- **Ramp** - Software Engineer internships (Emerging Talent)
- **Google** - Software Developer Intern positions

## Pinterest Scraper (Deprecated - Not Currently Active)

### Overview
The Pinterest scraper extracts job listings from Pinterest's careers page at `https://www.pinterestcareers.com/jobs/`.

**Note:** This scraper is documented but not currently active in the scheduler. It may be re-enabled in the future.

### Features
- Scrapes all job listings with pagination support
- Filters by team, employment type, and location
- Extracts job title, location, team, and URL
- Uses httpx and BeautifulSoup for reliable scraping
- Handles multiple pages automatically

### Usage

```python
from scrapers import PinterestScraper

# Create scraper with filters
scraper = PinterestScraper(team="Engineering")

# Scrape jobs
jobs = await scraper.scrape()
```

### Available Filters

#### Team Options:
- Engineering
- Design
- Product
- Marketing & Communications
- Sales
- Trust & Safety
- Finance
- Corporate Strategy
- Global Content Organization
- IT
- University

#### Employment Type Options:
- Intern
- Regular
- Temporary (Fixed Term)

#### Location Options:
- San Francisco
- New York
- Remote
- Remote - US
- Palo Alto
- Seattle
- Toronto
- Dublin
- And many more...

### Data Format

Each job dictionary contains:
```python
{
    "id": "pinterest_7166348",  # Unique ID with company prefix
    "company": "Pinterest",
    "title": "Software Engineer II, Android",
    "team": "Engineering",
    "location": "Toronto",
    "url": "https://www.pinterestcareers.com/jobs/7166348/...",
    "description": None  # Not fetched to keep scraping efficient
}
```

## Adding New Scrapers

To add a new company scraper:

1. Create a new file `{company}_scraper.py` in this directory
2. Implement a scraper class with an async `scrape()` method that returns a list of job dictionaries
3. Each job should have: `id`, `company`, `title`, `team`, `location`, `url`, `description`
4. Export the scraper in `__init__.py`
5. Add it to the scheduler in `app/scheduler.py`

### Example Template

```python
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict

class CompanyScraper:
    COMPANY_NAME = "Company"
    BASE_URL = "https://company.com/careers"
    
    async def scrape(self) -> List[Dict[str, str]]:
        jobs = []
        async with httpx.AsyncClient() as client:
            response = await client.get(self.BASE_URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract jobs from soup
            # ...
            
        return jobs
```


# Job Scrapers

This directory contains scrapers for various company job boards.

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


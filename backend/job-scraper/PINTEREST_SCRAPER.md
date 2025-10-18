# Pinterest Scraper Implementation

## Overview
Successfully implemented a Pinterest careers page scraper for the job-scraper service.

## What Was Built

### 1. Pinterest Scraper (`scrapers/pinterest_scraper.py`)
- **Technology**: httpx + BeautifulSoup (reliable and fast)
- **Features**:
  - Scrapes all job listings from Pinterest careers page
  - Supports filtering by team, employment type, and location
  - Automatic pagination support (handles multiple pages)
  - Extracts: job ID, title, team, location, and URL
  - Proper error handling and logging

### 2. Scraper Configuration
- **Base URL**: `https://www.pinterestcareers.com/jobs/`
- **Default Team Filter**: Engineering (70 jobs as of implementation)
- **Pagination**: Automatically detects and scrapes all pages

### 3. Integration with Job Scraper System
- Updated `scrapers/__init__.py` to export `PinterestScraper`
- Modified `app/scheduler.py` to use Pinterest scraper
- Scheduler runs every hour (configurable via `SCRAPE_INTERVAL_HOURS`)
- Jobs are stored in SQLite database with full tracking

## Data Format

Each scraped job includes:
```python
{
    "id": "pinterest_7166348",  # Unique ID: company_jobid
    "company": "Pinterest",
    "title": "Software Engineer II, Android",
    "team": "Engineering",
    "location": "Toronto",
    "url": "https://www.pinterestcareers.com/jobs/7166348/...",
    "description": None  # Not scraped for efficiency
}
```

## Testing Results

✅ Successfully scraped 70 Engineering jobs from Pinterest
✅ Proper pagination (4 pages)
✅ All job metadata extracted correctly
✅ No linter errors
✅ Proper error handling and logging

## API Endpoints (All Working)

1. **Get All Jobs**
   ```bash
   GET /api/jobs?company=Pinterest&active_only=true
   ```

2. **Get Job by ID**
   ```bash
   GET /api/jobs/pinterest_7166348
   ```

3. **Get New Jobs Today**
   ```bash
   GET /api/jobs/new/today?company=Pinterest
   ```

4. **Get Statistics**
   ```bash
   GET /api/stats
   ```

5. **Manual Scrape**
   ```bash
   POST /api/scrape?company=pinterest
   ```

## Filter Options Available

### Teams
- Engineering ✅ (default)
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

### Employment Types
- Regular
- Intern
- Temporary (Fixed Term)

### Locations
- San Francisco
- New York
- Remote
- Remote - US
- Toronto
- Dublin
- Palo Alto
- Seattle
- And many more...

## How to Use

### Basic Usage
```python
from scrapers import PinterestScraper

# Create scraper with filters
scraper = PinterestScraper(team="Engineering")

# Scrape jobs
jobs = await scraper.scrape()
print(f"Found {len(jobs)} jobs")
```

### With Custom Filters
```python
# Scrape Design internships in San Francisco
scraper = PinterestScraper(
    team="Design",
    employment_type="Intern",
    location="San Francisco"
)
jobs = await scraper.scrape()
```

## Files Modified/Created

1. **Created**:
   - `/backend/job-scraper/scrapers/pinterest_scraper.py` - Main scraper implementation
   - `/backend/job-scraper/scrapers/README.md` - Scrapers documentation

2. **Modified**:
   - `/backend/job-scraper/scrapers/__init__.py` - Export PinterestScraper
   - `/backend/job-scraper/app/scheduler.py` - Use Pinterest scraper
   - `/backend/job-scraper/README.md` - Updated documentation

3. **Deleted**:
   - Old scraper references (Stripe, Cohere, Super)

## Next Steps (Optional)

1. **Add More Companies**:
   - Stripe
   - Google
   - Meta
   - Shopify
   - etc.

2. **Enhanced Features**:
   - Job description scraping
   - Email notifications for new jobs
   - Advanced filtering in API
   - Job application tracking

3. **Production Ready**:
   - PostgreSQL database
   - Kubernetes deployment
   - Monitoring and alerts
   - Rate limiting

## Running the Service

### Local Development
```bash
cd backend/job-scraper
source venv/bin/activate
uvicorn app.main:app --reload --port 8001
```

### Docker
```bash
cd backend/job-scraper
docker-compose up --build
```

The service will:
1. Initialize the database
2. Run initial scrape
3. Start scheduler (runs every hour)
4. Serve API on port 8001

## Success Metrics

- ✅ Scraper working reliably
- ✅ All 70 Engineering jobs captured
- ✅ Proper deduplication by job ID
- ✅ Change tracking (first_seen, last_seen, is_active)
- ✅ RESTful API endpoints functional
- ✅ Clean code with no linter errors
- ✅ Comprehensive documentation


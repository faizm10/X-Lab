# Job Scraper Service

Automated job posting scraper that monitors company career pages and stores job listings.

## Features

- 🔍 **Automated Scraping**: Scrapes job postings every hour (configurable)
- 🏢 **Company Scrapers**: Currently supports Microsoft careers pages
- 🎯 **Smart Filtering**: Filter by profession, experience level, employment type, and location
- 📊 **Database Storage**: SQLite database for storing job postings
- 🚀 **REST API**: FastAPI endpoints for querying jobs
- 🐳 **Docker Support**: Fully containerized with Docker Compose
- 🔄 **Smart Deduplication**: Automatically deduplicates jobs by unique ID
- 📈 **Change Tracking**: Tracks when jobs are first seen, last seen, and when they become inactive

## Quick Start

### Local Development

1. **Install dependencies**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Run the service**:
```bash
uvicorn app.main:app --reload --port 8001
```

3. **Access the API**:
- API Docs: http://localhost:8001/docs
- Health Check: http://localhost:8001/health

### Docker Deployment

1. **Build and run with Docker Compose**:
```bash
docker-compose up --build
```

2. **Run in detached mode**:
```bash
docker-compose up -d
```

3. **View logs**:
```bash
docker-compose logs -f
```

4. **Stop the service**:
```bash
docker-compose down
```

## API Endpoints

### Get All Jobs
```bash
GET /api/jobs?company=Microsoft&active_only=true&limit=100&offset=0
```

### Get Job by ID
```bash
GET /api/jobs/{job_id}
```

### Get New Jobs Today
```bash
GET /api/jobs/new/today?company=Microsoft
```

### Get Statistics
```bash
GET /api/stats
```

### Manually Trigger Scrape
```bash
POST /api/scrape?company=microsoft
```

## Configuration

Environment variables (set in `.env` or docker-compose.yml):

- `DATABASE_URL`: Database connection string (default: `sqlite:///./data/jobs.db`)
- `SCRAPE_INTERVAL_HOURS`: Hours between scrapes (default: `1`)
- `API_PORT`: API server port (default: `8001`)
- `CORS_ORIGINS`: Comma-separated allowed origins (default: `http://localhost:3000`)

## Database Schema

### JobPosting Table
- `id` (String, PK): Unique job identifier
- `company` (String): Company name
- `title` (String): Job title
- `team` (String): Team/department
- `location` (String): Job location
- `url` (String): Link to job posting
- `description` (Text): Job description
- `first_seen` (DateTime): When job was first discovered by our scraper
- `last_seen` (DateTime): When job was last seen in a scrape
- `is_active` (Boolean): Whether job is currently active
- `posted_date` (DateTime): Original posting date from company website (extracted from API/website)
- `scraped_count` (Integer): Number of times scraped

**Note on Dates:**
- `posted_date`: The date when the company posted the job (from their website/API). May be `null` if not available.
- `first_seen`: The date when our scraper first discovered the job (our scraping time).
- `last_seen`: The date when our scraper last saw the job (updated on each scrape).

## Adding New Company Scrapers

To add a new company scraper:

1. Create a new scraper in `scrapers/` (e.g., `google_scraper.py`)
2. Inherit from a base scraper or implement similar interface
3. Add scraper to scheduler in `app/scheduler.py`
4. Update API endpoints as needed

Example scraper structure:
```python
class CompanyScraper:
    async def scrape(self, query: str) -> List[Dict]:
        # Implementation
        pass
```

## Testing

Test the scrapers directly:

### Microsoft Scraper
```python
import asyncio
from scrapers.microsoft_scraper import scrape_microsoft

async def test():
    jobs = await scrape_microsoft(
        professions=["Engineering", "Software Engineering"],
        experience="Students and graduates",
        employment_type="Internship"
    )
    print(f"Found {len(jobs)} jobs")

asyncio.run(test())
```

## Troubleshooting

### Database Issues
To reset the database:
```bash
rm data/jobs.db
# Restart the service to recreate tables
```

### Docker Issues
Rebuild containers:
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

## Supported Companies

- ✅ **Microsoft** - Full support via official API ([docs](MICROSOFT_SCRAPER.md))
  - API-based scraping (more reliable and faster)
  - Posting dates included directly in API response
  - Filters: profession, experience level, employment type, location
  - Default: Software Engineering internships for students and graduates

## Future Enhancements

- [ ] Add more company scrapers (Stripe, Google, Meta, Shopify, etc.)
- [ ] Email/Slack notifications for new jobs
- [ ] Job description scraping (currently only metadata)
- [ ] PostgreSQL support for production
- [ ] Job application tracking
- [ ] Advanced filtering and search
- [ ] Historical data visualization
- [ ] Auto-apply to jobs based on user preferences


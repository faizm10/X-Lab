# Job Scraper Service

Automated job posting scraper that monitors company career pages and stores job listings.

## Features

- 🔍 **Automated Scraping**: Scrapes job postings every hour (configurable)
- 🏢 **Company Scrapers**: Currently supports Pinterest careers page
- 🎯 **Team Filtering**: Filter by team (Engineering, Design, Product, etc.)
- 📍 **Location Filtering**: Filter by location (San Francisco, Remote, etc.)
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
GET /api/jobs?company=Pinterest&active_only=true&limit=100&offset=0
```

### Get Job by ID
```bash
GET /api/jobs/{job_id}
```

### Get New Jobs Today
```bash
GET /api/jobs/new/today?company=Pinterest
```

### Get Statistics
```bash
GET /api/stats
```

### Manually Trigger Scrape
```bash
POST /api/scrape?company=pinterest
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
- `first_seen` (DateTime): When job was first discovered
- `last_seen` (DateTime): When job was last seen in scrape
- `is_active` (Boolean): Whether job is currently active
- `posted_date` (DateTime): Original posting date
- `scraped_count` (Integer): Number of times scraped

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

Test the scraper directly:
```python
# Create a test script
import asyncio
from scrapers import PinterestScraper

async def test():
    scraper = PinterestScraper(team="Engineering")
    jobs = await scraper.scrape()
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

- ✅ **Pinterest** - Full support with team and location filtering

## Future Enhancements

- [ ] Add more company scrapers (Stripe, Google, Meta, Shopify, etc.)
- [ ] Email/Slack notifications for new jobs
- [ ] Job description scraping (currently only metadata)
- [ ] PostgreSQL support for production
- [ ] Job application tracking
- [ ] Advanced filtering and search
- [ ] Historical data visualization
- [ ] Auto-apply to jobs based on user preferences


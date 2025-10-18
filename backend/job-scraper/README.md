# Job Scraper Service

Automated job posting scraper that monitors company career pages and stores job listings.

## Features

- 🔍 **Automated Scraping**: Scrapes job postings every hour (configurable)
- 🎯 **Keyword-Based Search**: Searches Stripe's job board for exact keyword:
  - `intern` (exact word match only)
- 🇨🇦 **Location Filtering**: Only Canadian positions (Toronto, Vancouver, Ottawa, Montreal, Calgary, Edmonton, Remote in Canada)
- 📊 **Database Storage**: SQLite database for storing job postings
- 🚀 **REST API**: FastAPI endpoints for querying jobs
- 🐳 **Docker Support**: Fully containerized with Docker Compose
- 🔄 **Smart Deduplication**: Automatically deduplicates jobs found across multiple keyword searches
- 📈 **Change Tracking**: Tracks when jobs are first seen, last seen, and when they become inactive

## Quick Start

### Local Development

1. **Install dependencies**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
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
GET /api/jobs?company=Stripe&active_only=true&limit=100&offset=0
```

### Get Job by ID
```bash
GET /api/jobs/{job_id}
```

### Get New Jobs Today
```bash
GET /api/jobs/new/today?company=Stripe
```

### Get Statistics
```bash
GET /api/stats
```

### Manually Trigger Scrape
```bash
POST /api/scrape?company=stripe
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
```bash
python -m scrapers.stripe_scraper
```

## Troubleshooting

### Playwright Issues
If Playwright fails to install browsers:
```bash
playwright install --with-deps chromium
```

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

## Future Enhancements

- [ ] Add more company scrapers (Google, Meta, etc.)
- [ ] Email/Slack notifications for new jobs
- [ ] Job description analysis and keyword extraction
- [ ] PostgreSQL support for production
- [ ] Job application tracking
- [ ] Advanced filtering and search
- [ ] Historical data visualization


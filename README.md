# Faiz Lab

Personal experiments, data analysis projects, and automation tools.

## Projects

### 🔬 Labs (Research & Analysis)
- **GO Transit Costs**: Analyze cost/time tradeoffs for different commuting patterns
- **Referee Decision Bias**: Statistical analysis of officiating bias in football matches
- **Job Postings Analysis**: Web scraping and trend analysis of job market data

### 🛠️ Tools (Practical Utilities)
- **Automatic Job Alerts**: Real-time monitoring and notifications for new job postings

## Tech Stack

### Frontend
- **Next.js 15** with App Router
- **TypeScript**
- **Tailwind CSS**
- **Geist Font**

### Backend
- **FastAPI** (Python)
- **SQLAlchemy** ORM
- **Playwright** for web scraping
- **APScheduler** for job scheduling
- **SQLite** database

### Infrastructure
- **Docker** & **Docker Compose**
- Automated deployment
- Health checks and monitoring

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)

### Run Everything with Docker

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

Services will be available at:
- **Frontend**: http://localhost:3000
- **Job Scraper API**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs

### Local Development

#### Frontend (Next.js)

```bash
cd web
npm install
npm run dev
```

Frontend will be available at http://localhost:3000

#### Backend (Job Scraper)

```bash
cd backend/job-scraper
./run.sh
```

Or manually:

```bash
cd backend/job-scraper
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
uvicorn app.main:app --reload --port 8001
```

API will be available at http://localhost:8001

## Project Structure

```
faiz-lab/
├── web/                          # Next.js frontend
│   ├── src/
│   │   ├── app/                  # App router pages
│   │   │   ├── labs/            # Research projects
│   │   │   └── tools/           # Utility tools
│   │   ├── components/          # React components
│   │   ├── lib/                 # Utilities and API clients
│   │   └── data/                # Mock data and types
│   └── Dockerfile
│
├── backend/
│   ├── job-scraper/             # Job scraping service
│   │   ├── app/                 # FastAPI application
│   │   ├── models/              # Database models
│   │   ├── scrapers/            # Web scrapers
│   │   ├── data/                # SQLite database
│   │   └── Dockerfile
│   │
│   └── go-transit-costs/        # GO Transit analysis
│
└── docker-compose.yml           # Orchestration
```

## Features

### Automatic Job Alerts

- 🔍 **Automated Scraping**: Searches job boards every hour using specific keywords
- 🎯 **Keyword Search**: Searches for `intern` (exact word only)
- 🇨🇦 **Canada Only**: Filters for Canadian cities (Toronto, Vancouver, Ottawa, Montreal, etc.)
- 📊 **Database Storage**: Tracks job postings over time
- 🔄 **Smart Deduplication**: Combines results from multiple searches
- 📈 **Analytics**: Statistics on new jobs, trends, and patterns
- 🚀 **REST API**: Query jobs programmatically

#### API Endpoints

```bash
# Get all jobs
GET /api/jobs?company=Stripe&active_only=true&limit=100

# Filter by keywords (intern, internship, co-op, coop, software engineer, etc.)
GET /api/jobs?keywords=intern,internship,co-op,coop,software engineer,software engineering,software developer

# Get jobs first seen today
GET /api/jobs/new/today

# Get statistics
GET /api/stats

# Manually trigger scrape
POST /api/scrape?company=stripe
```

### Adding New Company Scrapers

1. Create a new scraper in `backend/job-scraper/scrapers/`
2. Follow the pattern in `stripe_scraper.py`
3. Add to scheduler in `app/scheduler.py`
4. Update API endpoints as needed

Example:

```python
class GoogleScraper:
    async def scrape(self, query: str) -> List[Dict]:
        # Implementation
        pass
```

## Environment Variables

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8001
```

### Backend (job-scraper)
```env
DATABASE_URL=sqlite:///./data/jobs.db
SCRAPE_INTERVAL_HOURS=1
API_PORT=8001
CORS_ORIGINS=http://localhost:3000
```

## Development

### Frontend Development

```bash
cd web
npm run dev        # Start dev server
npm run build      # Build for production
npm run lint       # Lint code
```

### Backend Development

```bash
cd backend/job-scraper

# Run tests
python -m pytest

# Test scraper directly
python -m scrapers.stripe_scraper

# Format code
black .
```

## Deployment

### Production Build

```bash
# Build all services
docker-compose build

# Run in production mode
docker-compose up -d

# View logs
docker-compose logs -f
```

### Health Checks

All services include health checks:
- Frontend: Next.js health endpoint
- Backend: `/health` endpoint

## Troubleshooting

### Playwright Issues
```bash
cd backend/job-scraper
playwright install --with-deps chromium
```

### Database Reset
```bash
rm backend/job-scraper/data/jobs.db
docker-compose restart job-scraper
```

### Docker Issues
```bash
docker-compose down
docker system prune -a
docker-compose build --no-cache
docker-compose up
```

## Future Enhancements

- [ ] Email/Slack notifications for new jobs
- [ ] More company scrapers (Google, Meta, Amazon, etc.)
- [ ] Job application tracking
- [ ] Advanced filtering and search
- [ ] Historical data visualization
- [ ] PostgreSQL for production
- [ ] Kubernetes deployment

## Contributing

This is a personal project, but feel free to fork and adapt for your own use!

## License

MIT License - Feel free to use and modify as needed.

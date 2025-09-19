# Faiz Labs Backend

FastAPI backend for Faiz Labs experiments and metrics.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /` - API info
- `GET /trips/recent?limit=20` - Get recent trips
- `GET /metrics/weekly?iso=YYYY-Www` - Get weekly metrics
- `GET /metrics/compare?iso=YYYY-Www` - Get comparison metrics
- `GET /metrics/latest-week` - Get latest available week

## Data

Trip data is stored in JSONL format in `data/trips/` directory. Each line contains a JSON object with:
- `ts`: timestamp (ISO format)
- `mode`: "train+bus" or "bus+bus"
- `route`: route description
- `cost`: cost in dollars
- `sched_time_min`: scheduled time in minutes
- `actual_time_min`: actual time in minutes

## Features

- File-backed data (no database required)
- LRU caching for performance
- CORS enabled for development
- Error handling for malformed data

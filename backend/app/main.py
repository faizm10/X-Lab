from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from app.services.metrics import (
    get_recent_trips, 
    get_weekly_metrics, 
    get_compare_metrics,
    get_latest_week
)

app = FastAPI(
    title="Faiz Labs API",
    description="Backend API for Faiz Labs experiments and metrics",
    version="1.0.0"
)

# Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Faiz Labs API", "version": "1.0.0"}


@app.get("/trips/recent")
async def get_recent_trips_endpoint(limit: int = 20):
    """Get the most recent trips sorted by timestamp descending."""
    try:
        trips = get_recent_trips(limit)
        return {"trips": trips, "count": len(trips)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching trips: {str(e)}")


@app.get("/metrics/weekly")
async def get_weekly_metrics_endpoint(iso: str):
    """Get weekly metrics for the specified ISO week (format: YYYY-Www)."""
    try:
        metrics = get_weekly_metrics(iso)
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating weekly metrics: {str(e)}")


@app.get("/metrics/compare")
async def get_compare_metrics_endpoint(iso: str):
    """Get comparison metrics and scenario analysis for the specified ISO week."""
    try:
        metrics = get_compare_metrics(iso)
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating compare metrics: {str(e)}")


@app.get("/metrics/latest-week")
async def get_latest_week_endpoint():
    """Get the latest week available in the data."""
    try:
        week = get_latest_week()
        return {"latest_week": week}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting latest week: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

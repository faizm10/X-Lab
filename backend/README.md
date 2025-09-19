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

## templates for trips
```json
{
  "ts": "YYYY-MM-DDThh:mm:ss-04:00",
  "mode": "train+bus | bus+bus",
  "route": "Origin → ... → Destination",
  "origin": "Start",
  "destination": "End",
  "segments": [
    {"type":"local_bus","from":"...","to":"...","fare":3.40},
    {"type":"go_train","from":"...","to":"...","tap_on":0.60,"fare":X.XX,"depart":"HH:MM","arrive":"HH:MM","sched_minutes":NN},
    {"type":"go_bus","from":"...","to":"...","fare":0.00,"transfer_free":true}
  ],
  "actual_cost": 0.00,
  "official_components": {"local_bus": 0.00, "go_point_to_point": 0.00},
  "official_fare_total": 0.00,
  "savings_abs": 0.00,
  "savings_pct": 0.0,
  "notes": ""
}
```
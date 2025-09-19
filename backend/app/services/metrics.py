from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dateutil import parser
import json
import os
from functools import lru_cache


@lru_cache(maxsize=128)
def load_trips_data() -> List[Dict[str, Any]]:
    """Load all trip data from JSONL files with caching."""
    trips = []
    data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "trips")
    
    if not os.path.exists(data_dir):
        return trips
    
    for filename in os.listdir(data_dir):
        if filename.endswith('.jsonl'):
            filepath = os.path.join(data_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                trip = json.loads(line)
                                trips.append(trip)
                            except json.JSONDecodeError:
                                continue  # Skip malformed lines
            except (IOError, OSError):
                continue  # Skip files that can't be read
    
    return trips


def get_recent_trips(limit: int = 20) -> List[Dict[str, Any]]:
    """Get the most recent trips sorted by timestamp descending."""
    trips = load_trips_data()
    
    # Sort by timestamp descending and limit
    sorted_trips = sorted(trips, key=lambda x: x.get('ts', ''), reverse=True)
    return sorted_trips[:limit]


def get_weekly_metrics(iso_week: str) -> Dict[str, Any]:
    """Calculate weekly metrics for the specified ISO week."""
    trips = load_trips_data()
    
    # Parse ISO week (format: YYYY-Www)
    year, week = iso_week.split('-W')
    year = int(year)
    week = int(week)
    
    # Get start of the week
    jan_1 = datetime(year, 1, 1)
    week_start = jan_1 + timedelta(weeks=week-1) - timedelta(days=jan_1.weekday())
    
    # Filter trips for this week
    week_trips = []
    for trip in trips:
        try:
            trip_time = parser.parse(trip['ts'])
            if week_start <= trip_time < week_start + timedelta(days=7):
                week_trips.append(trip)
        except (ValueError, KeyError):
            continue
    
    # Separate by mode
    train_bus_trips = [t for t in week_trips if t.get('mode') == 'train+bus']
    bus_bus_trips = [t for t in week_trips if t.get('mode') == 'bus+bus']
    
    def calculate_mode_metrics(trips: List[Dict[str, Any]]) -> Dict[str, float]:
        if not trips:
            return {
                'avg_cost': 0.0,
                'avg_time': 0.0,
                'avg_delay': 0.0,
                'cost_per_min': 0.0,
                'reliability': 0.0
            }
        
        total_cost = sum(t.get('cost', 0) for t in trips)
        total_time = sum(t.get('actual_time_min', 0) for t in trips)
        total_delay = sum(t.get('actual_time_min', 0) - t.get('sched_time_min', 0) for t in trips)
        
        avg_cost = total_cost / len(trips)
        avg_time = total_time / len(trips)
        avg_delay = total_delay / len(trips)
        cost_per_min = avg_cost / avg_time if avg_time > 0 else 0.0
        
        # Reliability: percentage of trips with delay <= 10 minutes
        on_time_trips = sum(1 for t in trips if (t.get('actual_time_min', 0) - t.get('sched_time_min', 0)) <= 10)
        reliability = on_time_trips / len(trips)
        
        return {
            'avg_cost': round(avg_cost, 1),
            'avg_time': round(avg_time, 1),
            'avg_delay': round(avg_delay, 1),
            'cost_per_min': round(cost_per_min, 2),
            'reliability': round(reliability, 2)
        }
    
    train_bus_metrics = calculate_mode_metrics(train_bus_trips)
    bus_bus_metrics = calculate_mode_metrics(bus_bus_trips)
    
    return {
        'week': iso_week,
        'avg_cost_train_bus': train_bus_metrics['avg_cost'],
        'avg_cost_bus_bus': bus_bus_metrics['avg_cost'],
        'avg_time_train_bus': train_bus_metrics['avg_time'],
        'avg_time_bus_bus': bus_bus_metrics['avg_time'],
        'avg_delay_train_bus': train_bus_metrics['avg_delay'],
        'avg_delay_bus_bus': bus_bus_metrics['avg_delay'],
        'cost_per_min_train_bus': train_bus_metrics['cost_per_min'],
        'cost_per_min_bus_bus': bus_bus_metrics['cost_per_min'],
        'reliability_train_bus': train_bus_metrics['reliability'],
        'reliability_bus_bus': bus_bus_metrics['reliability']
    }


def get_compare_metrics(iso_week: str) -> Dict[str, Any]:
    """Get comparison metrics and scenario analysis."""
    weekly_metrics = get_weekly_metrics(iso_week)
    
    # Calculate deltas
    delta_avg_cost = weekly_metrics['avg_cost_train_bus'] - weekly_metrics['avg_cost_bus_bus']
    delta_avg_time = weekly_metrics['avg_time_train_bus'] - weekly_metrics['avg_time_bus_bus']
    
    # Scenario: if all trips were bus+bus
    # Assuming 5 trips per week average
    trips_per_week = 5
    total_money_saved = delta_avg_cost * trips_per_week
    total_minutes_lost = -delta_avg_time * trips_per_week  # Negative because bus+bus takes longer
    
    # Value of time: how many minutes you save per dollar spent
    value_of_time = abs(delta_avg_time / delta_avg_cost) if delta_avg_cost > 0 else 0
    
    return {
        'iso_week': iso_week,
        'delta_avg_cost': round(delta_avg_cost, 1),
        'delta_avg_time_min': round(delta_avg_time, 1),
        'scenario_all_busbus': {
            'total_money_saved': round(total_money_saved, 1),
            'total_minutes_lost': round(total_minutes_lost, 1)
        },
        'value_of_time_minutes_per_dollar': round(value_of_time, 1)
    }


def get_latest_week() -> str:
    """Get the latest week available in the data."""
    trips = load_trips_data()
    if not trips:
        # Default to current week if no data
        from datetime import datetime
        now = datetime.now()
        year, week, _ = now.isocalendar()
        return f"{year}-W{week:02d}"
    
    # Find the latest timestamp
    latest_ts = max(trip.get('ts', '') for trip in trips)
    if latest_ts:
        trip_time = parser.parse(latest_ts)
        year, week, _ = trip_time.isocalendar()
        return f"{year}-W{week:02d}"
    
    # Fallback to current week
    from datetime import datetime
    now = datetime.now()
    year, week, _ = now.isocalendar()
    return f"{year}-W{week:02d}"

#!/usr/bin/env python3
"""
Export scraped jobs into a JSON file that the static frontend can consume.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from models import JobPosting
from models.database import SessionLocal


def serialize_job(job: JobPosting) -> dict:
    def _iso(value):
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.isoformat()
        return value

    return {
        "id": job.id,
        "company": job.company,
        "title": job.title,
        "location": job.location,
        "workModel": "hybrid",
        "team": job.team,
        "discipline": job.team,
        "description": job.description,
        "tags": [],
        "postedAt": _iso(job.posted_date) or _iso(job.first_seen),
        "applyUrl": job.url,
        "seniority": "internship",
        "isActive": job.is_active,
    }


def export_jobs(output: Path, include_inactive: bool = False) -> int:
    session = SessionLocal()
    try:
        query = session.query(JobPosting)
        if not include_inactive:
            query = query.filter(JobPosting.is_active == True)  # noqa: E712
        jobs = query.order_by(JobPosting.first_seen.desc()).all()

        data = [serialize_job(job) for job in jobs]

        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(data, indent=2))
        return len(data)
    finally:
        session.close()


def main():
    parser = argparse.ArgumentParser(description="Export scraped jobs to JSON")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "job-board" / "data" / "jobs.json",
        help="Destination JSON file",
    )
    parser.add_argument(
        "--include-inactive",
        action="store_true",
        help="Include inactive postings",
    )
    args = parser.parse_args()

    count = export_jobs(args.output, include_inactive=args.include_inactive)
    print(f"Exported {count} jobs to {args.output}")


if __name__ == "__main__":
    main()


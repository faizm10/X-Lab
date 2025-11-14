#!/usr/bin/env python3
"""
Run every scraper once and export the results to the static frontend.
"""
import argparse
import asyncio
from pathlib import Path

from app.scheduler import scrape_and_store_jobs
from export_jobs import export_jobs


async def main(output: Path, include_inactive: bool) -> None:
    await scrape_and_store_jobs()
    count = export_jobs(output, include_inactive=include_inactive)
    print(f"✅ Scrape finished. Wrote {count} jobs to {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "job-board" / "data" / "jobs.json",
    )
    parser.add_argument("--include-inactive", action="store_true")
    args = parser.parse_args()

    asyncio.run(main(args.output, args.include_inactive))


"""
Ramp Emerging Talent scraper
"""
from __future__ import annotations

import asyncio
import logging
import re
from typing import Dict, List, Optional

import httpx
from bs4 import BeautifulSoup, Tag

logger = logging.getLogger(__name__)


class RampScraper:
    """Scraper for Ramp Emerging Talent page, targeting SWE internships."""

    BASE_URL = "https://ramp.com"
    EMERGING_TALENT_URL = "https://ramp.com/emerging-talent"
    TARGET_PHRASE = "Software Engineer Internship"

    def __init__(self, session: Optional[httpx.AsyncClient] = None) -> None:
        self._session = session

    async def scrape(self) -> List[Dict[str, str]]:
        """Scrape Ramp Emerging Talent site for SWE internships."""
        created_session = False
        if self._session is None:
            self._session = httpx.AsyncClient(
                timeout=30,
                follow_redirects=True,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/126.0.0.0 Safari/537.36"
                    ),
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                },
            )
            created_session = True

        jobs: List[Dict[str, str]] = []
        try:
            logger.info("Scraping Ramp Emerging Talent page: %s", self.EMERGING_TALENT_URL)
            response = await self._session.get(self.EMERGING_TALENT_URL)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            jobs_section = soup.find(id="jobs") or soup
            jobs = self._extract_jobs(jobs_section)
            logger.info("Scraped %s Ramp SWE internship postings", len(jobs))
        except Exception as exc:  # pragma: no cover - log unexpected parsing issues
            logger.error("Error scraping Ramp Emerging Talent page: %s", exc)
            raise
        finally:
            if created_session and self._session:
                await self._session.aclose()

        return jobs

    def _extract_jobs(self, root: Tag) -> List[Dict[str, str]]:
        """Parse DOM tree for SWE internship postings."""
        postings: List[Dict[str, str]] = []
        seen_ids = set()

        job_links = root.find_all("a", href=True)
        for link in job_links:
            title_text = link.get_text(" ", strip=True)
            if not title_text:
                continue

            if self.TARGET_PHRASE.lower() not in title_text.lower():
                continue

            job_title = title_text
            if "|" in job_title:
                # Normalize "Software Engineer Internship | Frontend"
                parts = [part.strip() for part in job_title.split("|")]
                job_title = " | ".join(parts)

            location = self._find_location_near(link) or "New York, NY (HQ)"

            job_id = self._slugify(job_title)
            if job_id in seen_ids:
                continue

            job_url = link["href"]
            if job_url.startswith("/"):
                job_url = f"{self.BASE_URL}{job_url}"

            postings.append(
                {
                    "id": f"ramp_{job_id}",
                    "company": "Ramp",
                    "title": job_title,
                    "team": "Emerging Talent",
                    "location": location,
                    "url": job_url,
                    "description": None,
                    "posted_date": None,
                }
            )
            seen_ids.add(job_id)

        return postings

    def _find_location_near(self, node: Tag) -> Optional[str]:
        """Try to locate the text node containing the location near the job anchor."""
        location_pattern = re.compile(r"[A-Za-z .]+,\s?[A-Z]{2}|\(HQ\)|Remote", re.IGNORECASE)

        # Inspect siblings first
        for sibling in list(node.next_siblings)[:5]:
            text = self._extract_text(sibling)
            if text and location_pattern.search(text):
                return text.strip()

        # Fallback: walk up to parent and inspect its text content
        parent = node.parent
        if parent:
            text = parent.get_text(" ", strip=True)
            match = location_pattern.search(text)
            if match:
                return match.group(0)

        return None

    @staticmethod
    def _extract_text(element) -> Optional[str]:
        if element is None:
            return None
        if isinstance(element, str):
            return element.strip()
        if hasattr(element, "get_text"):
            return element.get_text(" ", strip=True)
        return None

    @staticmethod
    def _slugify(value: str) -> str:
        value = value.lower()
        value = re.sub(r"[^a-z0-9]+", "-", value)
        return value.strip("-")


if __name__ == "__main__":  # pragma: no cover - manual test helper
    async def _test():
        scraper = RampScraper()
        jobs = await scraper.scrape()
        for job in jobs:
            print(job)

    asyncio.run(_test())


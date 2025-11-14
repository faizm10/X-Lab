# Faiz Job Board (Static Frontend)

This folder contains a lightweight, data-first job board that mirrors the Faiz Lab visual language while removing the need for a hosted backend. Job postings are read directly from `job-board/data/jobs.json`, so you can add or remove entries by editing a single file and committing the change.

## Quick start

```bash
cd job-board
npm install
npm run dev
```

Build for production:

```bash
npm run build
npm run preview
```

## Updating job data manually

1. Open `job-board/data/jobs.json`
2. Duplicate an existing object or paste results exported from the backend scraper
3. Keep IDs unique (e.g., `company_role_year_city`)
4. Commit the change — Vercel, Netlify, or GitHub Pages can serve the static bundle

## Automated flow (recommended)

1. Run the FastAPI scrapers locally or within CI:

   ```bash
   python backend/job-scraper/scrape_and_export.py --output job-board/data/jobs.json
   ```

   This will:
   - Execute every scraper once (Microsoft, RBC, BMO, CIBC, Interac, Google)
   - Persist the results to SQLite
   - Export fresh data into the frontend JSON file

2. Commit the updated JSON (manually or via a GitHub Actions workflow)
3. Deploy the static site — no database or API hosting required

## GitHub Actions sketch

```yaml
name: Nightly job sync

on:
  schedule:
    - cron: "0 5 * * *" # 5am UTC
  workflow_dispatch:

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r backend/job-scraper/requirements.txt
      - run: python backend/job-scraper/scrape_and_export.py --output job-board/data/jobs.json
      - run: |
          git config user.name "faiz-bot"
          git config user.email "bot@users.noreply.github.com"
          if ! git diff --quiet job-board/data/jobs.json; then
            git commit -am "chore: refresh job data"
            git push
          else
            echo "No job data changes"
          fi
```

Pair this workflow with a static hosting provider (Vercel, Netlify, GitHub Pages) and the job board will auto-refresh nightly.


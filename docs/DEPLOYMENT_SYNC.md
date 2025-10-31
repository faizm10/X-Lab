# Deployment Synchronization Guide

## Problem: Localhost vs Deployed Discrepancy

When your localhost shows different companies than the deployed site, this usually indicates:

1. **Backend code mismatch**: The deployed backend is running different scheduler code
2. **Database state mismatch**: The deployed database has stale data from previous scraper configurations
3. **Deployment not triggered**: Changes to `backend/job-scraper/app/scheduler.py` require a Railway redeploy

---

## Root Cause

The companies shown in the frontend come from the database, which is populated by the scheduler in `backend/job-scraper/app/scheduler.py`. 

**Current Scheduler Configuration (as of latest code):**
- ✅ Microsoft (Engineering internships)
- ✅ RBC (Intern/Co-op positions)
- ✅ Google (Software Developer Intern positions)

**Companies mentioned but NOT in scheduler:**
- ❌ Pinterest (documented but scraper doesn't exist)
- ❌ BMO (no scraper exists)

If deployed site shows Microsoft/Pinterest but localhost shows Google/BMO, it means:
- Deployed backend has **old database data** from when different scrapers ran
- OR deployed backend is running **old scheduler code**

---

## Solution: Synchronize Deployments

### Step 1: Verify Current Scheduler Code

Check `backend/job-scraper/app/scheduler.py` to see which scrapers are currently configured:

```python
# Should include:
# - MicrosoftScraper
# - RBCScraper  
# - GoogleScraper
```

### Step 2: Ensure Code is Committed and Pushed

```bash
# Verify changes are committed
git status

# Push to main
git push origin main
```

### Step 3: Redeploy Backend on Railway

**Railway Auto-Deployment:**
- Railway should auto-deploy when code is pushed to `main`
- However, if the deployment doesn't trigger automatically, manually redeploy:

**Manual Redeploy:**
1. Go to **Railway Dashboard**
2. Select your **job-scraper** service
3. Go to **Deployments** tab
4. Click **"Deploy Latest"** or **"Redeploy"**

**OR via CLI:**
```bash
cd backend/job-scraper
railway up
```

### Step 4: Clear Old Database Data (If Needed)

If the deployed database has stale data from old scrapers, you have two options:

**Option A: Let it self-correct (Recommended)**
- The scheduler will mark inactive jobs after scraping
- Old companies will eventually disappear as jobs become inactive
- Wait 1-2 scrape cycles (1-2 hours)

**Option B: Clear specific company data via API**
```bash
# Delete all jobs for a specific company
curl -X DELETE https://your-backend.up.railway.app/api/jobs/company/Pinterest
curl -X DELETE https://your-backend.up.railway.app/api/jobs/company/BMO
```

**Option C: Reset entire database (Nuclear option)**
⚠️ **Warning**: This deletes ALL job data
1. In Railway Dashboard → Variables
2. Temporarily change `DATABASE_URL` to a new file
3. Redeploy
4. Change back to original `DATABASE_URL`
5. Redeploy again

---

## When Does Backend Need Redeployment?

### ✅ Backend REQUIRES Redeploy When:

1. **Scheduler changes** (`backend/job-scraper/app/scheduler.py`)
   - Adding/removing scrapers
   - Changing scraper parameters
   - Changing scrape intervals

2. **Model changes** (`backend/job-scraper/models/`)
   - Database schema changes
   - New fields added

3. **API endpoint changes** (`backend/job-scraper/app/main.py`)
   - New endpoints
   - Endpoint behavior changes

4. **New dependencies** (`backend/job-scraper/requirements.txt`)
   - New Python packages added

5. **Dockerfile changes** (`backend/job-scraper/Dockerfile`)

### ❌ Backend DOES NOT Need Redeploy For:

- Frontend changes (`web/` directory)
- Documentation changes (`docs/` directory)
- Script changes (`scripts/` directory)

---

## Verification Steps

After redeploying, verify the fix:

### 1. Check Backend Stats
```bash
curl https://your-backend.up.railway.app/api/stats
```

Should return:
```json
{
  "companies": ["Microsoft", "RBC", "Google"],
  "companies_tracked": 3,
  ...
}
```

### 2. Check Frontend
1. Visit deployed frontend
2. Go to `/labs/job-postings`
3. Check "Companies Tracked" section
4. Should match backend companies

### 3. Check Scheduler Logs
In Railway Dashboard → job-scraper service → Logs

Should see:
```
Starting scheduled scrape...
Scraped X internship jobs from Microsoft
Scraped Y intern/co-op jobs from RBC
Scraped Z software developer intern jobs from Google
```

---

## Quick Fix Checklist

When companies don't match between localhost and deployed:

- [ ] Verify `backend/job-scraper/app/scheduler.py` has correct scrapers
- [ ] Push latest code to `main` branch
- [ ] Check Railway deployment status (should auto-deploy)
- [ ] If needed, manually trigger Railway redeploy
- [ ] Wait for next scrape cycle (up to 1 hour)
- [ ] Verify `/api/stats` returns expected companies
- [ ] Check frontend displays correct companies
- [ ] If still wrong, clear old company data via API

---

## Preventing Future Issues

1. **Always commit scheduler changes before testing locally**
   ```bash
   git add backend/job-scraper/app/scheduler.py
   git commit -m "Update scheduler: add Google scraper"
   git push origin main
   ```

2. **Test locally first, then deploy**
   - Run scraper locally
   - Verify companies are correct
   - Then push to main

3. **Document scraper additions**
   - Update `backend/job-scraper/scrapers/README.md`
   - Update main `README.md` if needed

4. **Monitor Railway deployments**
   - Check Railway Dashboard after pushing
   - Verify deployment succeeds
   - Check logs for errors

---

## Troubleshooting

### Companies still don't match after redeploy

**Check 1: Is Railway using latest code?**
- Railway Dashboard → Deployments
- Check latest deployment commit hash
- Verify it matches your latest commit

**Check 2: Is scheduler actually running?**
```bash
curl https://your-backend.up.railway.app/api/stats
# Check "last_scraped" timestamp
# Should be within last hour
```

**Check 3: Are scrapers failing silently?**
- Check Railway logs for errors
- Look for: `Error scraping Microsoft`, `Error scraping Google`, etc.

### Railway not auto-deploying

1. **Check Railway project settings:**
   - Railway Dashboard → Project → Settings
   - Verify GitHub integration is connected
   - Verify branch is set to `main`

2. **Manually trigger deploy:**
   ```bash
   cd backend/job-scraper
   railway up
   ```

### Database has stale data

Use API to clean up:
```bash
# List all companies in database
curl https://your-backend.up.railway.app/api/stats | jq '.companies'

# Delete specific company
curl -X DELETE https://your-backend.up.railway.app/api/jobs/company/CompanyName
```

---

## Summary

**Key Takeaway:**
- Frontend shows companies from **database**, not code
- Database is populated by **scheduler** which runs scrapers
- When scheduler code changes, **backend must redeploy**
- Old database data may persist until cleared or naturally expires

**Fix Flow:**
1. Update scheduler code
2. Push to main
3. Railway redeploys (auto or manual)
4. Scheduler runs and updates database
5. Frontend reflects new companies


# Issue #17 Fix: Deployed Site Not Up to Date with Localhost

## Issue Summary

**Problem:** The deployed site shows different companies (Microsoft, Pinterest) than localhost (Google, BMO).

**Root Cause:** 
- The deployed Railway backend has stale database data from previous scraper configurations
- OR the deployed backend hasn't been redeployed after scheduler code changes
- The scheduler code in the repository currently includes: **Microsoft, RBC, and Google**
- Pinterest and BMO scrapers are **not implemented** in the current code

## Solution

### Step 1: Verify Current Scheduler Configuration

The scheduler in `backend/job-scraper/app/scheduler.py` currently includes:
- ✅ **Microsoft** - Engineering internships
- ✅ **RBC** - Intern/Co-op positions  
- ✅ **Google** - Software Developer Intern positions

### Step 2: Ensure Code is Synced

1. Verify your local code matches the repository:
   ```bash
   git status
   git pull origin main
   ```

2. Push any local changes:
   ```bash
   git add .
   git commit -m "Sync scheduler configuration"
   git push origin main
   ```

### Step 3: Redeploy Backend on Railway

**Option A: Auto-Deploy (if enabled)**
- Railway should automatically deploy when code is pushed to `main`
- Check Railway Dashboard → Deployments to verify

**Option B: Manual Deploy**
```bash
cd backend/job-scraper
railway up
```

**Option C: Via Railway Dashboard**
1. Go to Railway Dashboard
2. Select your job-scraper service
3. Go to Deployments tab
4. Click "Redeploy" or "Deploy Latest"

### Step 4: Clear Stale Database Data

The deployed database may have old data from Pinterest/BMO scrapers. You have two options:

**Option A: Wait for Natural Cleanup (Recommended)**
- The scheduler will mark inactive jobs after the next scrape cycle
- Old companies (Pinterest, BMO) will disappear as their jobs become inactive
- Wait 1-2 scrape cycles (1-2 hours)

**Option B: Manual Cleanup via API**
```bash
# Replace with your Railway backend URL
BACKEND_URL="https://your-backend.up.railway.app"

# Delete Pinterest jobs (if they exist)
curl -X DELETE $BACKEND_URL/api/jobs/company/Pinterest

# Delete BMO jobs (if they exist)
curl -X DELETE $BACKEND_URL/api/jobs/company/BMO
```

### Step 5: Verify Fix

1. **Check Backend Stats:**
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

2. **Check Frontend:**
   - Visit your deployed site
   - Navigate to `/labs/job-postings`
   - Verify "Companies Tracked" shows: Microsoft, RBC, Google

3. **Check Scheduler Logs:**
   - Railway Dashboard → job-scraper service → Logs
   - Should see logs for Microsoft, RBC, and Google scrapers

## Why This Happened

1. **Database Persistence:** Railway uses SQLite database stored in a volume, so old data persists across deployments
2. **Stale Scraper Data:** Previous versions may have included Pinterest/BMO scrapers that were later removed
3. **Deployment Timing:** If scheduler code changed but backend wasn't redeployed, old scrapers would continue running

## Prevention

To prevent this in the future:

1. **Always redeploy backend when scheduler changes:**
   - After modifying `backend/job-scraper/app/scheduler.py`
   - Push to `main`
   - Verify Railway auto-deploys or manually trigger

2. **Document scraper additions/removals:**
   - Update `backend/job-scraper/scrapers/README.md`
   - Update main `README.md` if needed

3. **Verify deployment after changes:**
   - Check Railway logs to see which scrapers are running
   - Check `/api/stats` endpoint to see which companies are tracked

## Related Documentation

- **Full Deployment Sync Guide:** `docs/DEPLOYMENT_SYNC.md`
- **Deployment Checklist:** `docs/DEPLOYMENT_CHECKLIST.md`
- **Production Configuration:** `docs/PRODUCTION_CONFIG.md`

## Quick Reference

**Current Scheduled Companies:** Microsoft, RBC, Google  
**Companies NOT in code:** Pinterest, BMO  
**Backend Deployment:** Railway (auto or manual)  
**Database Cleanup:** Wait for natural expiration OR use API DELETE endpoint

---

**Status:** ✅ Fixed - Backend redeployment and database cleanup required


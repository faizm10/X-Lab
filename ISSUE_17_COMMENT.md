# GitHub Issue #17 Comment - Fix Explanation

---

Hey @faizm10! 👋

I've investigated the discrepancy between localhost and the deployed site, and I've found the root cause. Here's what's happening and how we're fixing it:

## What Was Wrong

The deployed Railway backend has **stale database data** from previous scraper configurations. The frontend shows companies from whatever data is in the database, and right now:

- **Deployed site** shows: Microsoft, Pinterest (from old database)
- **Localhost** shows: Google, BMO (from your local database)

However, the **actual scheduler code** in the repository currently includes:
- ✅ Microsoft (Engineering internships)
- ✅ RBC (Intern/Co-op positions)
- ✅ Google (Software Developer Intern positions)

Pinterest and BMO scrapers aren't actually in the current codebase - they're either leftover from previous versions or were never implemented but got added to the database somehow.

## The Fix

I've done two things:

1. **Created comprehensive documentation** to prevent this in the future:
   - `docs/DEPLOYMENT_SYNC.md` - Full guide on syncing localhost and deployed versions
   - `docs/ISSUE_17_FIX.md` - Step-by-step fix for this specific issue
   - Updated `docs/DEPLOYMENT_CHECKLIST.md` with backend redeployment requirements

2. **Updated the scheduler docstring** to accurately reflect all three scrapers (Microsoft, RBC, Google)

## What We Need To Do Now

### Step 1: Pull latest from main (to avoid conflicts)
```bash
git pull origin main
```

### Step 2: Push the documentation and fixes
```bash
git add .
git commit -m "Fix #17: Add deployment sync documentation and clarify scheduler configuration"
git push origin main
```

### Step 3: Redeploy Backend on Railway

Railway should auto-deploy when we push to `main`, but to be safe:

**Option A:** Check Railway Dashboard → Deployments to verify auto-deploy triggered

**Option B:** Manually trigger redeploy:
- Railway Dashboard → job-scraper service → Deployments → "Redeploy"
- OR via CLI: `cd backend/job-scraper && railway up`

### Step 4: Clear Stale Database Data

The deployed database still has old Pinterest data. We can either:

**Option A (Recommended):** Wait 1-2 hours for natural cleanup
- The scheduler will mark Pinterest jobs as inactive after the next scrape cycle

**Option B (Immediate):** Manually delete via API
```bash
curl -X DELETE https://your-backend.up.railway.app/api/jobs/company/Pinterest
```

### Step 5: Verify

After redeploying, check:
1. Railway logs should show Microsoft, RBC, and Google scrapers running
2. `/api/stats` should return: `{"companies": ["Microsoft", "RBC", "Google"], ...}`
3. Deployed frontend should show the same three companies

## Why This Happened

When the scheduler code changes (adding/removing scrapers), the **backend must be redeployed** for the changes to take effect. The database persists across deployments, so old company data sticks around until:
- Jobs naturally become inactive (after scrapers stop running them)
- Or we manually clean them up

## Prevention

I've documented in `docs/DEPLOYMENT_SYNC.md` that whenever you modify `backend/job-scraper/app/scheduler.py`, you need to:
1. Push to `main`
2. Verify Railway redeploys (or manually trigger)
3. Check logs to confirm new scrapers are running

This should prevent this issue from happening again! 🎯

---

**Next Steps:**
- [ ] Pull latest from main
- [ ] Push these changes
- [ ] Redeploy backend on Railway
- [ ] Clear stale Pinterest data (if needed)
- [ ] Verify deployed site shows correct companies

Let me know once you've pushed and I can help verify the fix! 🚀


# Deployment Checklist - Vercel + Railway

This checklist ensures your frontend (Vercel) properly connects to your backend (Railway).

## Prerequisites
- [ ] Railway account created
- [ ] Vercel account created
- [ ] GitHub repository connected to both platforms

---

## 1. Backend Deployment (Railway)

### Step 1: Deploy Backend to Railway

```bash
# From your project root
cd backend/job-scraper

# Deploy to Railway (if not already done)
railway login
railway init
railway up
```

### Step 2: Configure Railway Environment Variables

Go to **Railway Dashboard** → Your Project → **job-scraper service** → **Variables**

Add these variables:

```bash
DATABASE_URL=sqlite:///./data/jobs.db
SCRAPE_INTERVAL_HOURS=1
CORS_ORIGINS=https://faiz-lab.vercel.app,https://faiz-lab-git-*.vercel.app
PORT=8001
```

**Important Notes:**
- Replace `https://faiz-lab.vercel.app` with your actual Vercel domain
- Add preview deployment domains (e.g., `https://faiz-lab-git-*.vercel.app`) to CORS_ORIGINS
- Railway automatically assigns a public URL - note this down!

### Step 3: Get Your Railway Backend URL

After deployment, Railway provides a public URL like:
```
https://your-service-name.up.railway.app
```

**Copy this URL** - you'll need it for Vercel configuration.

---

## 2. Frontend Deployment (Vercel)

### Step 1: Deploy to Vercel

```bash
cd web

# Deploy to Vercel
vercel

# For production
vercel --prod
```

Or connect your GitHub repository in the Vercel Dashboard for automatic deployments.

### Step 2: Configure Vercel Environment Variables

Go to **Vercel Dashboard** → Your Project → **Settings** → **Environment Variables**

Add the following variable:

| Name | Value | Environment |
|------|-------|-------------|
| `NEXT_PUBLIC_API_URL` | `https://your-service-name.up.railway.app` | Production, Preview, Development |

**Replace** `https://your-service-name.up.railway.app` with your actual Railway URL from Step 1.3.

### Step 3: Update vercel.json (Optional)

If you want to use path rewrites instead of environment variables, update `/web/vercel.json`:

```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://your-service-name.up.railway.app/api/:path*"
    }
  ]
}
```

Replace the destination URL with your Railway backend URL.

### Step 4: Redeploy Frontend

After adding environment variables:

```bash
# Trigger a new deployment
vercel --prod

# Or in Vercel Dashboard: Deployments → ... → Redeploy
```

---

## 3. Backend Redeployment After Code Changes

**IMPORTANT:** When you make changes to backend code (especially scheduler), Railway needs to redeploy.

### When Backend MUST Redeploy:

- ✅ Changes to `backend/job-scraper/app/scheduler.py` (adding/removing scrapers)
- ✅ Changes to `backend/job-scraper/app/main.py` (API endpoints)
- ✅ Changes to `backend/job-scraper/models/` (database schema)
- ✅ Changes to `backend/job-scraper/requirements.txt` (dependencies)
- ✅ Changes to `backend/job-scraper/Dockerfile`

### Railway Auto-Deployment:

Railway should automatically deploy when you push to `main` branch. However:

1. **Check deployment status:**
   - Railway Dashboard → Deployments
   - Verify latest commit is deployed

2. **If auto-deploy didn't trigger:**
   ```bash
   cd backend/job-scraper
   railway up
   ```

### Verifying Scheduler Changes:

After redeploying, check the backend logs to verify scrapers are running:

**Railway Dashboard** → job-scraper service → Logs

You should see:
```
Starting scheduled scrape...
Scraped X internship jobs from Microsoft
Scraped Y intern/co-op jobs from RBC
Scraped Z software developer intern jobs from Google
```

### If Companies Don't Match Between Localhost and Deployed:

This usually means the deployed database has stale data. See `docs/DEPLOYMENT_SYNC.md` for detailed troubleshooting.

**Quick fix:**
1. Verify scheduler code matches what you expect
2. Ensure code is pushed to `main`
3. Manually trigger Railway redeploy if needed
4. Wait for next scrape cycle (up to 1 hour)

---

## 4. Verification

### Test Backend (Railway)

```bash
# Health check
curl https://your-service-name.up.railway.app/health

# Test API endpoints
curl https://your-service-name.up.railway.app/api/stats
curl https://your-service-name.up.railway.app/api/jobs
```

Expected response for `/health`:
```json
{"status": "healthy"}
```

### Test Frontend (Vercel)

1. **Visit your Vercel URL:** `https://faiz-lab.vercel.app`
2. **Navigate to:** `/tools/automatic-job-alerts`
3. **Check the stats load:** Total Postings, New Today, etc. should display numbers (not "...")
4. **Check the console:** Open browser DevTools → Console
   - Should NOT see CORS errors
   - Should NOT see network errors fetching from API

### Test CORS

Open browser console on your Vercel site and run:

```javascript
fetch('https://your-service-name.up.railway.app/api/stats')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error)
```

Should see stats data, NOT a CORS error.

---

## 5. Update Railway CORS When Vercel URL Changes

If your Vercel URL changes, update Railway's `CORS_ORIGINS`:

**Railway Dashboard** → Variables → `CORS_ORIGINS`:
```
https://your-new-vercel-url.vercel.app,https://faiz-lab-git-*.vercel.app
```

Then redeploy the backend service.

---

## 6. Common Issues & Troubleshooting

### ❌ Frontend shows "Failed to fetch" errors

**Cause:** `NEXT_PUBLIC_API_URL` not set in Vercel

**Fix:**
1. Go to Vercel Dashboard → Settings → Environment Variables
2. Add `NEXT_PUBLIC_API_URL` with your Railway URL
3. Redeploy

### ❌ CORS errors in browser console

**Cause:** Railway backend doesn't allow your Vercel domain

**Fix:**
1. Go to Railway Dashboard → Variables → `CORS_ORIGINS`
2. Add your Vercel domain (e.g., `https://faiz-lab.vercel.app`)
3. Include preview domains: `https://faiz-lab-git-*.vercel.app`
4. Redeploy backend

### ❌ Stats showing "..." but no errors

**Cause:** API calls timing out or backend not responding

**Fix:**
1. Check Railway backend logs: Railway Dashboard → Deployments → Logs
2. Verify backend is running: `curl https://your-backend.up.railway.app/health`
3. Check Railway service hasn't gone to sleep (free tier)

### ❌ Environment variable not taking effect

**Cause:** Vercel caches builds

**Fix:**
1. After adding/changing env vars, trigger a new deployment
2. In Vercel Dashboard: Deployments → ... → Redeploy
3. Or push a new commit to trigger auto-deployment

---

## 7. URLs Quick Reference

Fill these in after deployment:

| Service | URL | Notes |
|---------|-----|-------|
| **Railway Backend** | `https://_____.up.railway.app` | Add to Vercel env vars |
| **Vercel Frontend** | `https://_____.vercel.app` | Add to Railway CORS_ORIGINS |
| **Vercel Preview** | `https://_____-git-*.vercel.app` | Add to Railway CORS_ORIGINS |

---

## 8. Environment Variables Summary

### Railway (Backend)
```bash
DATABASE_URL=sqlite:///./data/jobs.db
SCRAPE_INTERVAL_HOURS=1
CORS_ORIGINS=https://your-frontend.vercel.app,https://your-frontend-git-*.vercel.app
PORT=8001  # Railway auto-assigns if not set
```

### Vercel (Frontend)
```bash
NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app
```

---

## ✅ Deployment Complete!

Once all steps are completed:
- ✅ Backend is deployed to Railway
- ✅ Frontend is deployed to Vercel
- ✅ Environment variables are configured
- ✅ CORS is properly set up
- ✅ API calls work from production frontend
- ✅ Both services can communicate

Visit your Vercel URL and test the job alerts page!


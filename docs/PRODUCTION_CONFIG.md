# Production Configuration Reference

Quick reference for production deployment environment variables.

## 🎯 TL;DR - What You Need to Do

### 1. Vercel (Frontend)
In **Vercel Dashboard** → **Settings** → **Environment Variables**, add:

```
NEXT_PUBLIC_API_URL=https://your-railway-backend-url.up.railway.app
```

### 2. Railway (Backend)  
In **Railway Dashboard** → **Variables**, add:

```
DATABASE_URL=sqlite:///./data/jobs.db
SCRAPE_INTERVAL_HOURS=1
CORS_ORIGINS=https://faiz-lab.vercel.app,https://faiz-lab-git-*.vercel.app,https://faiz-lab-*.vercel.app
PORT=8001
```

### 3. Redeploy Both Services
After setting environment variables, trigger new deployments for changes to take effect.

---

## 📋 Complete Configuration

### Vercel Environment Variables

| Variable | Value | Notes |
|----------|-------|-------|
| `NEXT_PUBLIC_API_URL` | `https://your-backend.up.railway.app` | **Required** - Your Railway backend URL |

**Where to add:**
1. Go to Vercel Dashboard
2. Select your project (faiz-lab-web or similar)
3. Go to Settings → Environment Variables
4. Add the variable
5. Select: Production, Preview, Development (all three)
6. Save

**After adding:** Redeploy your Vercel app for changes to take effect.

---

### Railway Environment Variables

| Variable | Value | Notes |
|----------|-------|-------|
| `DATABASE_URL` | `sqlite:///./data/jobs.db` | Can switch to PostgreSQL later |
| `SCRAPE_INTERVAL_HOURS` | `1` | How often to scrape (in hours) |
| `CORS_ORIGINS` | `https://faiz-lab.vercel.app,https://faiz-lab-git-*.vercel.app,https://faiz-lab-*.vercel.app` | **Required** - Your Vercel URLs |
| `PORT` | `8001` | Railway may auto-assign, but explicit is better |

**Where to add:**
1. Go to Railway Dashboard
2. Select your job-scraper service
3. Go to Variables tab
4. Add each variable
5. Save

**After adding:** Deploy will auto-trigger, or manually trigger a new deployment.

---

## 🔍 How to Find Your URLs

### Railway Backend URL

1. Railway Dashboard → Your Project → job-scraper service
2. Look for **Settings** → **Domains**
3. Your public URL is shown there
4. Example: `https://job-scraper-production-a1b2.up.railway.app`

**Copy this URL** → Use it for Vercel's `NEXT_PUBLIC_API_URL`

### Vercel Frontend URL

1. Vercel Dashboard → Your Project
2. Look for **Domains** in the project overview
3. Your production URL is shown there
4. Example: `https://faiz-lab.vercel.app`

**Copy this URL** → Use it for Railway's `CORS_ORIGINS`

---

## ✅ Verification Checklist

After configuring environment variables:

### Backend (Railway)

```bash
# Test health endpoint
curl https://your-backend.up.railway.app/health

# Should return:
# {"status":"healthy"}

# Test API endpoint  
curl https://your-backend.up.railway.app/api/stats

# Should return JSON with stats data
```

### Frontend (Vercel)

1. Visit: `https://your-frontend.vercel.app/tools/automatic-job-alerts`
2. Check that stats load (numbers appear, not "...")
3. Check that job listings appear
4. Open browser console (F12)
5. Look for errors:
   - ❌ **No CORS errors** should appear
   - ❌ **No "Failed to fetch"** errors should appear
   - ✅ **Network requests** should be going to your Railway URL

### Test CORS

In browser console on your Vercel site:

```javascript
fetch('https://your-backend.up.railway.app/api/stats')
  .then(r => r.json())
  .then(data => console.log('✅ Success:', data))
  .catch(err => console.error('❌ Error:', err))
```

Should see `✅ Success:` with data, not a CORS error.

---

## 🚨 Common Issues

### Issue: Frontend shows "Failed to fetch"

**Cause:** `NEXT_PUBLIC_API_URL` not set in Vercel

**Fix:**
1. Add the environment variable in Vercel Dashboard
2. Redeploy the frontend
3. Hard refresh browser (Cmd+Shift+R)

### Issue: CORS error in browser console

**Error message:**
```
Access to fetch at 'https://...' from origin 'https://...' has been blocked by CORS policy
```

**Cause:** Railway backend doesn't allow your Vercel domain

**Fix:**
1. Update `CORS_ORIGINS` in Railway Dashboard
2. Include your Vercel production URL
3. Include preview deployment URLs with wildcard (e.g., `https://faiz-lab-*.vercel.app`)
4. Redeploy backend

### Issue: Environment variable not working

**Cause:** Changes only apply after new deployment

**Fix:**
- **Vercel:** Go to Deployments → Click ... → Redeploy
- **Railway:** Usually auto-deploys when you change variables, or manually trigger redeploy

### Issue: Backend not responding

**Cause:** Backend service might be sleeping (Railway free tier)

**Fix:**
1. Check Railway Dashboard → Deployments → Status
2. Check logs for errors
3. Verify backend is actually running
4. Consider upgrading Railway plan to prevent sleeping

---

## 📖 Additional Resources

- **Complete Deployment Guide:** See `DEPLOYMENT.md`
- **Step-by-Step Checklist:** See `DEPLOYMENT_CHECKLIST.md`
- **Vercel Setup Guide:** See `VERCEL_SETUP.md`

---

## 🆘 Still Having Issues?

1. **Check Railway Logs:**
   - Railway Dashboard → Deployments → Select latest deployment → View Logs
   - Look for errors or startup issues

2. **Check Vercel Logs:**
   - Vercel Dashboard → Deployments → Select latest deployment → View Function Logs
   - Check build logs for issues

3. **Browser Console:**
   - Open DevTools (F12)
   - Check Console tab for errors
   - Check Network tab to see what URLs are being called

4. **Verify Environment Variables:**
   - **Vercel:** Settings → Environment Variables
   - **Railway:** Your Service → Variables
   - Make sure they're saved and deployment was triggered

---

## 📝 Quick Copy-Paste Templates

### For Vercel Dashboard

```
Variable Name: NEXT_PUBLIC_API_URL
Value: [PASTE YOUR RAILWAY URL HERE]
Environments: Production, Preview, Development (all selected)
```

### For Railway Dashboard

```
DATABASE_URL=sqlite:///./data/jobs.db
SCRAPE_INTERVAL_HOURS=1
CORS_ORIGINS=[PASTE YOUR VERCEL URL HERE],https://faiz-lab-git-*.vercel.app,https://faiz-lab-*.vercel.app
PORT=8001
```

**Remember to:**
- Replace `[PASTE YOUR RAILWAY URL HERE]` with actual Railway backend URL
- Replace `[PASTE YOUR VERCEL URL HERE]` with actual Vercel frontend URL
- Don't include trailing slashes
- Redeploy both services after adding variables


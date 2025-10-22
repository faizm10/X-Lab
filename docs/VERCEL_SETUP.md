# Vercel Frontend Setup Guide

## Quick Setup: Environment Variables

To ensure your Vercel frontend fetches from your Railway backend, you **MUST** configure this environment variable in Vercel:

### 🚨 Required Vercel Environment Variable

Go to: **Vercel Dashboard** → **Your Project** → **Settings** → **Environment Variables**

Add this variable:

```
Name:  NEXT_PUBLIC_API_URL
Value: https://your-backend-service.up.railway.app
Environment: Production, Preview, Development (check all three)
```

### How to Find Your Railway Backend URL

1. Go to **Railway Dashboard**
2. Click on your **job-scraper** service
3. Go to **Settings** tab
4. Under **Domains**, you'll see your public URL
5. It looks like: `https://job-scraper-production-XXXX.up.railway.app`

**Copy this exact URL** and use it as the value for `NEXT_PUBLIC_API_URL` in Vercel.

---

## After Adding the Environment Variable

**Important:** Environment variables only take effect after a new deployment.

### Option 1: Redeploy in Vercel Dashboard
1. Go to **Deployments** tab
2. Click the **...** menu on your latest deployment  
3. Click **Redeploy**
4. Wait for deployment to complete

### Option 2: Push a New Commit
```bash
git commit --allow-empty -m "Trigger Vercel redeploy"
git push origin main
```

---

## Verification

### 1. Check Environment Variable is Set

After deployment, visit:
```
https://your-vercel-app.vercel.app/tools/automatic-job-alerts
```

Open browser console (F12) and run:
```javascript
console.log('API URL:', process.env.NEXT_PUBLIC_API_URL);
```

### 2. Test API Connection

On the job alerts page:
- ✅ Stats should load (Total Postings, New Today, etc.)
- ✅ Job listings should appear
- ❌ Should NOT see "Failed to fetch" errors
- ❌ Should NOT see CORS errors in console

### 3. Network Tab Check

Open DevTools → Network tab:
- Look for requests to `/api/stats`, `/api/jobs`
- They should be calling your Railway URL
- Response should be 200 OK with JSON data

---

## Troubleshooting

### ❌ Still seeing "Failed to fetch" errors

**Problem:** Environment variable not applied

**Solutions:**
1. Double-check the variable name is exactly: `NEXT_PUBLIC_API_URL` (case-sensitive)
2. Ensure it's set for all environments (Production, Preview, Development)
3. Trigger a new deployment (see "After Adding the Environment Variable" above)
4. Clear browser cache and hard reload (Cmd+Shift+R / Ctrl+Shift+F5)

### ❌ CORS errors in console

**Problem:** Railway backend is blocking your Vercel domain

**Solution:**
1. Go to Railway Dashboard → Variables
2. Update `CORS_ORIGINS` to include:
   ```
   https://faiz-lab.vercel.app,https://faiz-lab-git-*.vercel.app,https://faiz-lab-*.vercel.app
   ```
3. Redeploy the Railway backend service

### ❌ API URL is showing "http://localhost:8001"

**Problem:** Environment variable is not set in Vercel

**Solution:**
1. The frontend falls back to localhost when `NEXT_PUBLIC_API_URL` is not set
2. Add the variable in Vercel Dashboard (see top of this guide)
3. Redeploy

---

## Current Configuration Summary

### ✅ What's Already Configured

**Frontend Code (`web/src/lib/api.ts`):**
```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001";
```
✅ Already set up to use environment variable

**Vercel Config (`web/vercel.json`):**
✅ Created with security headers

**Railway Config (`backend/job-scraper/railway-env.txt`):**
✅ CORS configured to accept Vercel domains

### ❗ What You Need to Do

1. **Deploy Backend to Railway** (if not already done)
   - Note down the Railway URL
   
2. **Add Environment Variable in Vercel:**
   - Name: `NEXT_PUBLIC_API_URL`
   - Value: Your Railway backend URL
   - Environments: All (Production, Preview, Development)
   
3. **Redeploy Vercel** to apply the environment variable

4. **Test** the production site to verify it's working

---

## Example URLs

After deployment, your setup should look like:

| Service | Example URL |
|---------|-------------|
| Railway Backend | `https://job-scraper-production-a1b2.up.railway.app` |
| Vercel Frontend | `https://faiz-lab.vercel.app` |
| API Calls From Frontend | `https://job-scraper-production-a1b2.up.railway.app/api/stats` |

The frontend will automatically use the `NEXT_PUBLIC_API_URL` for all API calls.

---

## Need Help?

If you're still having issues:

1. Check Railway logs: Railway Dashboard → Deployments → View Logs
2. Check Vercel logs: Vercel Dashboard → Deployments → View Function Logs  
3. Check browser console for specific error messages
4. Verify environment variables are set correctly in both platforms

**Common mistake:** Using the wrong Railway URL. Make sure you're using the public domain from Railway's Settings → Domains, not an internal URL.


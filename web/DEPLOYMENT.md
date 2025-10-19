# Frontend Deployment Instructions

## Deploying to Vercel

### Prerequisites
- Railway backend must be deployed first
- You need the Railway backend URL

### Required Environment Variable

**CRITICAL:** You must set this environment variable in Vercel for the frontend to work:

```
NEXT_PUBLIC_API_URL=https://your-backend-service.up.railway.app
```

### Steps to Deploy

#### 1. Deploy to Vercel

**Option A: Vercel CLI**
```bash
npm install -g vercel
cd web
vercel
```

**Option B: Vercel Dashboard**
- Connect your GitHub repository
- Select the `web` directory as the root directory
- Vercel will auto-deploy on push

#### 2. Configure Environment Variable

1. Go to **Vercel Dashboard**
2. Select your project
3. Go to **Settings** → **Environment Variables**
4. Add new variable:
   - **Name:** `NEXT_PUBLIC_API_URL`
   - **Value:** Your Railway backend URL (e.g., `https://job-scraper-production-xyz.up.railway.app`)
   - **Environments:** Select all (Production, Preview, Development)
5. Click **Save**

#### 3. Redeploy

After adding the environment variable, trigger a new deployment:

**Option A: In Vercel Dashboard**
- Go to **Deployments** tab
- Click the **...** menu on the latest deployment
- Click **Redeploy**

**Option B: Push a commit**
```bash
git commit --allow-empty -m "Trigger redeploy with env vars"
git push
```

### Verification

1. Visit your Vercel URL: `https://your-app.vercel.app`
2. Navigate to: `/tools/automatic-job-alerts`
3. Verify:
   - ✅ Stats load (Total Postings, New Today show numbers)
   - ✅ Job listings appear
   - ✅ No errors in browser console
   - ✅ No CORS errors

### Testing the API Connection

Open browser console on your deployed site and run:

```javascript
// This should show your Railway URL, not localhost
console.log('API URL:', process.env.NEXT_PUBLIC_API_URL);

// This should fetch data successfully
fetch('/api/stats')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);
```

### Troubleshooting

#### Stats showing "..." (not loading)

**Problem:** Environment variable not set or wrong value

**Solution:**
1. Check Vercel Dashboard → Settings → Environment Variables
2. Verify `NEXT_PUBLIC_API_URL` is set correctly
3. Make sure it's a full URL including `https://`
4. Redeploy after making changes

#### CORS Errors

**Problem:** Backend not allowing your Vercel domain

**Solution:**
1. Go to Railway Dashboard → Variables
2. Update `CORS_ORIGINS` to include your Vercel URL:
   ```
   https://your-app.vercel.app,https://your-app-*.vercel.app
   ```
3. Redeploy Railway backend

#### API calls going to localhost

**Problem:** Environment variable not applied

**Solution:**
1. Environment variables are only available at **build time** for `NEXT_PUBLIC_*` vars
2. You must redeploy after adding/changing the variable
3. Clear browser cache and hard reload

### Important Notes

- `NEXT_PUBLIC_API_URL` must start with `https://` in production
- Don't include trailing slashes in URLs
- The backend URL comes from Railway's public domain (Settings → Domains)
- Changes to environment variables require a new deployment to take effect
- Preview deployments also need the env var set (select "Preview" when adding)

### Example Configuration

```bash
# Development (local)
NEXT_PUBLIC_API_URL=http://localhost:8001

# Production (Vercel)
NEXT_PUBLIC_API_URL=https://job-scraper-production-a1b2.up.railway.app
```

### Need Help?

See the full deployment guides:
- `../PRODUCTION_CONFIG.md` - Quick reference for all environment variables
- `../VERCEL_SETUP.md` - Detailed Vercel setup guide
- `../DEPLOYMENT_CHECKLIST.md` - Complete deployment checklist
- `../DEPLOYMENT.md` - Comprehensive deployment guide


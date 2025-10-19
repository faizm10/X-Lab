# Deployment Guide

This guide covers deployment options for the Faiz Lab project, which consists of:
- **Frontend**: Next.js application (`/web`)
- **Backend**: FastAPI job scraper service (`/backend/job-scraper`)

## Table of Contents
1. [Current Structure](#current-structure)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Production Deployment Options](#production-deployment-options)
5. [Environment Variables](#environment-variables)
6. [Database Considerations](#database-considerations)
7. [Recommended Production Stack](#recommended-production-stack)

---

## Current Structure

```
faiz-lab/
├── docker-compose.yml          # Full stack orchestration
├── web/                        # Next.js frontend
│   ├── Dockerfile
│   └── package.json
└── backend/
    └── job-scraper/           # FastAPI backend
        ├── Dockerfile
        ├── docker-compose.yml  # Standalone backend
        └── requirements.txt
```

### Services

| Service | Technology | Port | Purpose |
|---------|-----------|------|---------|
| Frontend | Next.js 15 | 3000 | Web UI |
| Backend | FastAPI + Python 3.11 | 8001 | Job scraper API |

---

## Local Development

### Option 1: Docker (Recommended)
```bash
# Setup and run everything
./setup.sh

# Or manually
docker-compose up --build

# Access:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8001
# API Docs: http://localhost:8001/docs
```

### Option 2: Native Development
```bash
# Setup
./setup.sh
# Choose option 2 when prompted

# Run services (in separate terminals)
./start-dev.sh

# Or manually:
# Terminal 1 - Backend
cd backend/job-scraper
source venv/bin/activate
uvicorn app.main:app --reload --port 8001

# Terminal 2 - Frontend
cd web
npm run dev
```

---

## Docker Deployment

### Development (with hot reload)
```bash
docker-compose up --build
```

### Production (optimized builds)

**Issues with current Dockerfiles:**
1. Backend uses `--reload` flag (development only)
2. Frontend doesn't have multi-stage build optimization
3. No production environment variables
4. SQLite database in container (not persistent across deployments)

**Recommended fixes:**

#### 1. Update Backend Dockerfile for Production

```dockerfile
# backend/job-scraper/Dockerfile.prod
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p /app/data

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=40s \
  CMD curl -f http://localhost:8001/health || exit 1

# Expose port
EXPOSE 8001

# Production command (no reload)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "2"]
```

#### 2. Update Frontend Dockerfile for Production

```dockerfile
# web/Dockerfile.prod
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```

#### 3. Update docker-compose for Production

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  job-scraper:
    build:
      context: ./backend/job-scraper
      dockerfile: Dockerfile.prod
    container_name: faiz-lab-job-scraper
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=${DATABASE_URL:-sqlite:///./data/jobs.db}
      - SCRAPE_INTERVAL_HOURS=${SCRAPE_INTERVAL_HOURS:-1}
      - API_PORT=8001
      - CORS_ORIGINS=${CORS_ORIGINS}
    volumes:
      - job-data:/app/data
    restart: always
    networks:
      - faiz-lab-network

  web:
    build:
      context: ./web
      dockerfile: Dockerfile.prod
    container_name: faiz-lab-web
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
    depends_on:
      - job-scraper
    restart: always
    networks:
      - faiz-lab-network

volumes:
  job-data:
    driver: local

networks:
  faiz-lab-network:
    driver: bridge
```

---

## Production Deployment Options

### 🚀 Option 1: Vercel (Frontend) + Railway/Render (Backend)

**Best for:** Quick deployment, minimal DevOps

#### Frontend on Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd web
vercel

# Set environment variable
vercel env add NEXT_PUBLIC_API_URL
```

**Vercel Configuration:**
- Auto-deploys from Git
- Automatic HTTPS
- Global CDN
- Zero configuration needed

#### Backend on Railway
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
cd backend/job-scraper
railway login
railway init
railway up
```

**Railway Configuration:**
- Add PostgreSQL database (recommended over SQLite)
- Set environment variables:
  - `DATABASE_URL` (provided by Railway if using their PostgreSQL)
  - `CORS_ORIGINS` (your Vercel domain)
  - `SCRAPE_INTERVAL_HOURS`

**Pros:**
- ✅ Easiest to deploy
- ✅ Automatic SSL
- ✅ Git-based deployments
- ✅ Free tier available

**Cons:**
- ❌ More expensive at scale
- ❌ Less control over infrastructure

---

### 🐳 Option 2: DigitalOcean App Platform

**Best for:** Managed Docker deployment

```bash
# Install doctl
brew install doctl

# Deploy
doctl apps create --spec .do/app.yaml
```

**App Spec (`.do/app.yaml`):**
```yaml
name: faiz-lab
services:
  - name: web
    github:
      repo: your-username/faiz-lab
      branch: main
      deploy_on_push: true
    source_dir: /web
    build_command: npm run build
    run_command: npm start
    envs:
      - key: NEXT_PUBLIC_API_URL
        value: ${job-scraper.PUBLIC_URL}
    http_port: 3000
    
  - name: job-scraper
    github:
      repo: your-username/faiz-lab
      branch: main
      deploy_on_push: true
    source_dir: /backend/job-scraper
    dockerfile_path: /backend/job-scraper/Dockerfile.prod
    envs:
      - key: DATABASE_URL
        value: ${db.DATABASE_URL}
      - key: CORS_ORIGINS
        value: ${web.PUBLIC_URL}
      - key: SCRAPE_INTERVAL_HOURS
        value: "1"
    http_port: 8001

databases:
  - name: db
    engine: PG
    version: "15"
```

**Pros:**
- ✅ Managed Docker hosting
- ✅ Built-in database
- ✅ Automatic SSL
- ✅ Reasonably priced

**Cons:**
- ❌ Less flexible than raw VPS
- ❌ Vendor lock-in

---

### 🖥️ Option 3: VPS (DigitalOcean, AWS EC2, Hetzner)

**Best for:** Full control, cost optimization

**Setup Steps:**

1. **Provision Server**
   ```bash
   # Create droplet/instance with Docker
   # Ubuntu 22.04 LTS recommended
   ```

2. **Install Dependencies**
   ```bash
   ssh root@your-server

   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh

   # Install Docker Compose
   apt install docker-compose-plugin
   ```

3. **Setup Application**
   ```bash
   # Clone repo
   git clone https://github.com/your-username/faiz-lab.git
   cd faiz-lab

   # Create .env file
   cat > .env << EOF
   DATABASE_URL=postgresql://user:pass@localhost:5432/jobs
   CORS_ORIGINS=https://yourdomain.com
   SCRAPE_INTERVAL_HOURS=1
   NEXT_PUBLIC_API_URL=https://api.yourdomain.com
   EOF

   # Deploy
   docker-compose -f docker-compose.prod.yml up -d
   ```

4. **Setup Reverse Proxy (Nginx + Let's Encrypt)**
   ```bash
   # Install Nginx
   apt install nginx certbot python3-certbot-nginx

   # Configure Nginx
   cat > /etc/nginx/sites-available/faiz-lab << 'EOF'
   server {
       server_name yourdomain.com;
       location / {
           proxy_pass http://localhost:3000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }

   server {
       server_name api.yourdomain.com;
       location / {
           proxy_pass http://localhost:8001;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   EOF

   ln -s /etc/nginx/sites-available/faiz-lab /etc/nginx/sites-enabled/
   nginx -t
   systemctl reload nginx

   # Get SSL certificates
   certbot --nginx -d yourdomain.com -d api.yourdomain.com
   ```

**Pros:**
- ✅ Full control
- ✅ Most cost-effective at scale
- ✅ No vendor lock-in

**Cons:**
- ❌ More DevOps work
- ❌ You manage security/updates
- ❌ No automatic scaling

---

## Environment Variables

### Backend (`backend/job-scraper`)

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | Database connection string | `sqlite:///./data/jobs.db` | No |
| `SCRAPE_INTERVAL_HOURS` | Hours between scrapes | `1` | No |
| `API_PORT` | Port for API server | `8001` | No |
| `CORS_ORIGINS` | Allowed origins (comma-separated) | `http://localhost:3000` | Yes (prod) |

### Frontend (`web`)

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8001` | Yes |

---

## Database Considerations

### Current: SQLite
- ✅ Simple, no setup
- ✅ Perfect for development
- ❌ Not ideal for production
- ❌ Difficult to backup in containers
- ❌ Lost when container restarts (unless using volumes)

### Recommended for Production: PostgreSQL

**Why PostgreSQL:**
- ✅ Better concurrency
- ✅ More reliable for production
- ✅ Easy to backup
- ✅ Managed options available (RDS, Railway, Supabase)

**Migration Steps:**

1. **Update requirements.txt:**
   ```txt
   psycopg2-binary==2.9.9
   ```

2. **Update DATABASE_URL:**
   ```bash
   # Local PostgreSQL
   DATABASE_URL=postgresql://user:password@localhost:5432/jobs

   # Managed service (Railway, Supabase, RDS)
   DATABASE_URL=postgresql://user:password@host:5432/jobs?sslmode=require
   ```

3. **No code changes needed!** SQLAlchemy handles both SQLite and PostgreSQL.

---

## Recommended Production Stack

### 🏆 Best Overall: Hybrid Approach

```
Frontend:  Vercel (free tier, auto-scaling, global CDN)
Backend:   Railway or Render (managed, PostgreSQL included)
Database:  Managed PostgreSQL (included with Railway/Render)
Monitoring: Sentry (error tracking), Better Stack (uptime)
```

**Monthly Cost Estimate:**
- Vercel: $0 (hobby) or $20/mo (pro)
- Railway: $5-20/mo (depending on usage)
- **Total: ~$5-40/mo**

### Cost-Optimized: VPS

```
Server:    Hetzner VPS ($5/mo) or DigitalOcean Droplet ($6/mo)
Setup:     Docker + Nginx + Let's Encrypt
Database:  PostgreSQL on same server
Backups:   Daily automated backups to S3 ($1/mo)
```

**Monthly Cost Estimate: $6-10/mo**

---

## Quick Start Commands

### Deploy to Production (VPS)
```bash
# 1. Create production files
cp docker-compose.yml docker-compose.prod.yml
# Edit docker-compose.prod.yml (remove --reload, add workers)

# 2. Deploy
docker-compose -f docker-compose.prod.yml up -d --build

# 3. View logs
docker-compose -f docker-compose.prod.yml logs -f

# 4. Update application
git pull
docker-compose -f docker-compose.prod.yml up -d --build
```

### Health Checks
```bash
# Check backend
curl http://localhost:8001/health

# Check frontend
curl http://localhost:3000

# View backend logs
docker logs faiz-lab-job-scraper

# View frontend logs
docker logs faiz-lab-web
```

---

## Monitoring & Maintenance

### Backup Database
```bash
# SQLite
docker exec faiz-lab-job-scraper cp /app/data/jobs.db /app/data/jobs-backup-$(date +%Y%m%d).db

# PostgreSQL
pg_dump $DATABASE_URL > backup-$(date +%Y%m%d).sql
```

### Update Application
```bash
git pull
docker-compose -f docker-compose.prod.yml up -d --build
```

### View Scraper Status
```bash
# Check last scrape
curl http://localhost:8001/api/stats | jq '.last_scraped'

# Manually trigger scrape
curl -X POST http://localhost:8001/api/scrape
```

---

## Troubleshooting

### Frontend can't reach backend
- Check `NEXT_PUBLIC_API_URL` is set correctly
- Verify CORS origins in backend
- Check network connectivity

### Scraper not running
- Check logs: `docker logs faiz-lab-job-scraper`
- Verify `SCRAPE_INTERVAL_HOURS` is set
- Check if database is accessible

### Database connection errors
- Verify `DATABASE_URL` format
- Check database is running
- Ensure database exists and schema is created

---

## Next Steps

1. ✅ Choose deployment platform
2. ✅ Set up PostgreSQL (recommended)
3. ✅ Configure environment variables
4. ✅ Create production Dockerfiles
5. ✅ Set up monitoring
6. ✅ Configure backups
7. ✅ Set up CI/CD (GitHub Actions)


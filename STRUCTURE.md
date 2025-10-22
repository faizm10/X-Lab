# Project Structure

Clean and organized folder structure for the Faiz Lab monorepo.

## Directory Layout

```
faiz-lab/
├── 📁 backend/              # Backend services
│   ├── job-scraper/         # FastAPI job scraping service
│   └── README.md
│
├── 📁 web/                  # Next.js frontend application
│   ├── src/                 # Source code
│   ├── public/              # Static assets
│   ├── Dockerfile           # Development container
│   └── Dockerfile.prod      # Production container
│
├── 📁 docs/                 # All documentation
│   ├── README.md            # Documentation index
│   ├── DEPLOYMENT.md        # Deployment guide
│   ├── DEPLOYMENT_CHECKLIST.md
│   ├── PRODUCTION_CONFIG.md
│   └── VERCEL_SETUP.md
│
├── 📁 scripts/              # Utility scripts
│   ├── README.md            # Scripts documentation
│   ├── setup.sh             # Project setup
│   ├── start-dev.sh         # Start development
│   ├── test-cors.sh         # Test CORS
│   ├── test-deployment.sh   # Test endpoints
│   └── verify-deployment.sh # Verify production
│
├── 📄 README.md             # Main project documentation
├── 📄 .gitignore            # Git ignore rules
├── 📄 env.example           # Environment template
├── 📄 docker-compose.yml    # Development compose
└── 📄 docker-compose.prod.yml # Production compose
```

## Organization Principles

### 1. Clear Separation
- **Code**: `backend/` and `web/`
- **Documentation**: `docs/`
- **Scripts**: `scripts/`
- **Configuration**: Root level

### 2. Self-Documenting
Each major directory has its own README explaining:
- Purpose
- Contents
- Usage
- Examples

### 3. Logical Grouping
- All deployment docs in `docs/`
- All utility scripts in `scripts/`
- All configuration files at root level

### 4. Production Ready
- Separate production Docker files
- Environment templates
- Deployment verification scripts

## Quick Navigation

### For Development
- Start here: [README.md](./README.md)
- Setup: `./scripts/setup.sh`
- Run: `./scripts/start-dev.sh`

### For Deployment
- Guide: [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md)
- Checklist: [docs/DEPLOYMENT_CHECKLIST.md](./docs/DEPLOYMENT_CHECKLIST.md)
- Verify: `./scripts/verify-deployment.sh`

### For Configuration
- Environment: [env.example](./env.example)
- Production: [docs/PRODUCTION_CONFIG.md](./docs/PRODUCTION_CONFIG.md)

## Benefits

✅ **Clean Root** - Only essential files at root level  
✅ **Easy Navigation** - Clear folder names and structure  
✅ **Self-Documented** - README in each major directory  
✅ **Scalable** - Easy to add new services or docs  
✅ **Professional** - Industry-standard organization  

## Maintenance

To keep the structure clean:
1. **Docs** → Always go in `docs/`
2. **Scripts** → Always go in `scripts/`
3. **New services** → Add to `backend/` or `web/`
4. **Root files** → Only essential config files


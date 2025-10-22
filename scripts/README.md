# Scripts

Utility scripts for development, testing, and deployment.

## Scripts

### [setup.sh](./setup.sh)
**Purpose**: Initial project setup  
**Usage**: `./scripts/setup.sh`

Sets up the development environment:
- Installs frontend dependencies (npm)
- Installs backend dependencies (pip)
- Installs Playwright browsers
- Creates necessary directories
- Sets up environment files

### [start-dev.sh](./start-dev.sh)
**Purpose**: Start development environment  
**Usage**: `./scripts/start-dev.sh`

Starts both frontend and backend in development mode:
- Activates Python virtual environment
- Starts FastAPI backend on port 8001
- Starts Next.js frontend on port 3000
- Runs both services concurrently

### [test-cors.sh](./test-cors.sh)
**Purpose**: Test CORS configuration  
**Usage**: `./scripts/test-cors.sh [URL]`

Tests if CORS is properly configured:
- Sends OPTIONS preflight request
- Checks CORS headers
- Validates allowed origins
- Default URL: http://localhost:8001

**Example**:
```bash
./scripts/test-cors.sh https://your-backend.up.railway.app
```

### [test-deployment.sh](./test-deployment.sh)
**Purpose**: Test deployment endpoints  
**Usage**: `./scripts/test-deployment.sh`

Tests that all API endpoints are working:
- Health check endpoint
- Root endpoint
- Jobs API
- Stats API
- Reports any failures

### [verify-deployment.sh](./verify-deployment.sh)
**Purpose**: Comprehensive production deployment verification  
**Usage**: `./scripts/verify-deployment.sh`

Verifies production deployment:
- Checks frontend is accessible
- Verifies backend API is responding
- Tests CORS configuration
- Validates environment variables
- Checks database connectivity
- Tests API endpoints
- Generates deployment report

## Usage Tips

### Make scripts executable
```bash
chmod +x scripts/*.sh
```

### Run from project root
All scripts should be run from the project root directory:
```bash
./scripts/setup.sh
./scripts/start-dev.sh
```

### Environment variables
Some scripts may require environment variables to be set. Check the script comments for details.

## Troubleshooting

### Permission denied
If you get permission errors:
```bash
chmod +x scripts/*.sh
```

### Script not found
Make sure you're in the project root directory:
```bash
cd /path/to/faiz-lab
./scripts/script-name.sh
```

### Dependencies missing
Run the setup script first:
```bash
./scripts/setup.sh
```


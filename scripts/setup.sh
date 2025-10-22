#!/bin/bash

# Faiz Lab Setup Script
# This script sets up the entire project for local development

set -e

echo "🚀 Faiz Lab Setup"
echo "=================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker not found. Please install Docker first.${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker Compose not found. Please install Docker Compose first.${NC}"
    exit 1
fi

echo -e "${BLUE}🐳 Docker and Docker Compose found!${NC}"
echo ""

# Ask user how they want to run
echo "How would you like to run the project?"
echo "1) Docker (recommended - all services)"
echo "2) Local development (frontend + backend separately)"
read -p "Enter choice [1-2]: " choice

case $choice in
    1)
        echo ""
        echo -e "${BLUE}📦 Building and starting Docker containers...${NC}"
        docker-compose up --build -d
        
        echo ""
        echo -e "${GREEN}✅ Services started successfully!${NC}"
        echo ""
        echo "Services:"
        echo "  - Frontend:  http://localhost:3000"
        echo "  - API:       http://localhost:8001"
        echo "  - API Docs:  http://localhost:8001/docs"
        echo ""
        echo "To view logs:"
        echo "  docker-compose logs -f"
        echo ""
        echo "To stop:"
        echo "  docker-compose down"
        ;;
        
    2)
        echo ""
        echo -e "${BLUE}🔧 Setting up for local development...${NC}"
        echo ""
        
        # Setup backend
        echo -e "${BLUE}📦 Setting up backend...${NC}"
        cd backend/job-scraper
        
        if [ ! -d "venv" ]; then
            echo "Creating Python virtual environment..."
            python3 -m venv venv
        fi
        
        echo "Activating virtual environment and installing dependencies..."
        source venv/bin/activate
        pip install -q --upgrade pip
        pip install -q -r requirements.txt
        
        echo "Installing Playwright browsers..."
        playwright install chromium
        
        echo -e "${GREEN}✅ Backend setup complete${NC}"
        cd ../..
        
        # Setup frontend
        echo ""
        echo -e "${BLUE}📦 Setting up frontend...${NC}"
        cd web
        
        if [ ! -d "node_modules" ]; then
            echo "Installing npm dependencies..."
            npm install
        fi
        
        # Create .env.local if it doesn't exist
        if [ ! -f ".env.local" ]; then
            echo "Creating .env.local..."
            echo "NEXT_PUBLIC_API_URL=http://localhost:8001" > .env.local
        fi
        
        echo -e "${GREEN}✅ Frontend setup complete${NC}"
        cd ..
        
        echo ""
        echo -e "${GREEN}✅ Setup complete!${NC}"
        echo ""
        echo "To start the backend:"
        echo "  cd backend/job-scraper"
        echo "  source venv/bin/activate"
        echo "  uvicorn app.main:app --reload --port 8001"
        echo ""
        echo "To start the frontend:"
        echo "  cd web"
        echo "  npm run dev"
        echo ""
        echo "Or use the convenience script:"
        echo "  ./start-dev.sh"
        ;;
        
    *)
        echo -e "${YELLOW}Invalid choice. Exiting.${NC}"
        exit 1
        ;;
esac


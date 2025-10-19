#!/bin/bash

# Script to run the job scraper service locally

echo "🚀 Starting Job Scraper Service..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo "🎭 Installing Playwright browsers..."
playwright install chromium

# Create data directory if it doesn't exist
mkdir -p data

# Start the server
echo "✅ Starting server on http://localhost:8001"
echo "📚 API docs available at http://localhost:8001/docs"
echo ""
uvicorn app.main:app --reload --port 8001


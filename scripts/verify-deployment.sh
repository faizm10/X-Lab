#!/bin/bash

# Deployment Verification Script
# This script helps verify that your production deployment is configured correctly

echo "🔍 Verifying Deployment Configuration..."
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check URL
check_url() {
    local url=$1
    local name=$2
    
    echo -n "Testing $name... "
    
    if response=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$url" 2>/dev/null); then
        if [ "$response" -eq 200 ]; then
            echo -e "${GREEN}✅ OK (HTTP $response)${NC}"
            return 0
        else
            echo -e "${RED}❌ FAILED (HTTP $response)${NC}"
            return 1
        fi
    else
        echo -e "${RED}❌ FAILED (Connection error)${NC}"
        return 1
    fi
}

# Function to check JSON response
check_json_endpoint() {
    local url=$1
    local name=$2
    
    echo -n "Testing $name... "
    
    if response=$(curl -s --max-time 10 "$url" 2>/dev/null); then
        if echo "$response" | jq . >/dev/null 2>&1; then
            echo -e "${GREEN}✅ OK (Valid JSON)${NC}"
            echo "$response" | jq . | head -n 5
            return 0
        else
            echo -e "${RED}❌ FAILED (Invalid JSON response)${NC}"
            echo "Response: $response"
            return 1
        fi
    else
        echo -e "${RED}❌ FAILED (Connection error)${NC}"
        return 1
    fi
}

# Prompt for URLs
echo "Enter your URLs (press Enter to skip):"
echo ""

read -p "Backend URL (Railway): " BACKEND_URL
read -p "Frontend URL (Vercel): " FRONTEND_URL

echo ""
echo "=========================================="
echo ""

# Check if URLs are provided
if [ -z "$BACKEND_URL" ]; then
    echo -e "${YELLOW}⚠️  No backend URL provided, skipping backend tests${NC}"
    SKIP_BACKEND=1
else
    # Remove trailing slash
    BACKEND_URL=${BACKEND_URL%/}
fi

if [ -z "$FRONTEND_URL" ]; then
    echo -e "${YELLOW}⚠️  No frontend URL provided, skipping frontend tests${NC}"
    SKIP_FRONTEND=1
else
    # Remove trailing slash
    FRONTEND_URL=${FRONTEND_URL%/}
fi

echo ""

# Test Backend
if [ -z "$SKIP_BACKEND" ]; then
    echo "📡 Testing Backend (Railway)"
    echo "----------------------------"
    
    check_url "$BACKEND_URL/health" "Health endpoint"
    check_json_endpoint "$BACKEND_URL/api/stats" "Stats API"
    check_json_endpoint "$BACKEND_URL/api/jobs?limit=1" "Jobs API"
    
    echo ""
fi

# Test Frontend
if [ -z "$SKIP_FRONTEND" ]; then
    echo "🌐 Testing Frontend (Vercel)"
    echo "----------------------------"
    
    check_url "$FRONTEND_URL" "Homepage"
    check_url "$FRONTEND_URL/tools/automatic-job-alerts" "Job Alerts Page"
    
    echo ""
fi

# Test CORS
if [ -z "$SKIP_BACKEND" ] && [ -z "$SKIP_FRONTEND" ]; then
    echo "🔒 Testing CORS Configuration"
    echo "------------------------------"
    
    echo -n "Testing CORS headers... "
    
    cors_response=$(curl -s -I -X OPTIONS \
        -H "Origin: $FRONTEND_URL" \
        -H "Access-Control-Request-Method: GET" \
        "$BACKEND_URL/api/stats" 2>/dev/null)
    
    if echo "$cors_response" | grep -q "access-control-allow-origin"; then
        echo -e "${GREEN}✅ CORS headers present${NC}"
        echo "$cors_response" | grep -i "access-control"
    else
        echo -e "${RED}❌ CORS headers missing${NC}"
        echo -e "${YELLOW}Make sure CORS_ORIGINS in Railway includes: $FRONTEND_URL${NC}"
    fi
    
    echo ""
fi

# Configuration Summary
echo "📋 Configuration Summary"
echo "------------------------"

if [ -z "$SKIP_BACKEND" ]; then
    echo -e "${GREEN}Backend URL:${NC} $BACKEND_URL"
    echo ""
    echo "Railway Environment Variables should be:"
    echo "  DATABASE_URL=sqlite:///./data/jobs.db"
    echo "  SCRAPE_INTERVAL_HOURS=1"
    if [ ! -z "$FRONTEND_URL" ]; then
        echo "  CORS_ORIGINS=$FRONTEND_URL,${FRONTEND_URL/https:\/\//https://}-git-*.vercel.app"
    fi
    echo "  PORT=8001"
    echo ""
fi

if [ -z "$SKIP_FRONTEND" ]; then
    echo -e "${GREEN}Frontend URL:${NC} $FRONTEND_URL"
    echo ""
    echo "Vercel Environment Variables should be:"
    if [ ! -z "$BACKEND_URL" ]; then
        echo "  NEXT_PUBLIC_API_URL=$BACKEND_URL"
    else
        echo "  NEXT_PUBLIC_API_URL=https://your-backend-url.up.railway.app"
    fi
    echo ""
fi

# Final recommendations
echo "=========================================="
echo ""
echo "📚 Next Steps:"
echo ""

if [ -z "$SKIP_BACKEND" ]; then
    echo "1. Verify Railway environment variables are set correctly"
    echo "   → Railway Dashboard → Variables tab"
    echo ""
fi

if [ -z "$SKIP_FRONTEND" ]; then
    echo "2. Verify Vercel environment variables are set correctly"
    echo "   → Vercel Dashboard → Settings → Environment Variables"
    echo ""
fi

echo "3. After setting environment variables, redeploy both services"
echo ""

echo "4. Test the live application:"
if [ ! -z "$FRONTEND_URL" ]; then
    echo "   → Visit: $FRONTEND_URL/tools/automatic-job-alerts"
fi
echo "   → Check browser console for errors (F12)"
echo "   → Verify stats and jobs load successfully"
echo ""

echo "📖 For detailed instructions, see:"
echo "   - PRODUCTION_CONFIG.md (quick reference)"
echo "   - VERCEL_SETUP.md (step-by-step Vercel setup)"
echo "   - DEPLOYMENT_CHECKLIST.md (complete checklist)"
echo ""

echo "✅ Verification complete!"


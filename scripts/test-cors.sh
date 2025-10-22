#!/bin/bash

# Test CORS configuration
echo "🔒 Testing CORS Configuration"
echo "=============================="
echo ""

BACKEND_URL="https://faiz-lab-production.up.railway.app"
FRONTEND_URL="https://faiz-lab.vercel.app"

echo "Backend:  $BACKEND_URL"
echo "Frontend: $FRONTEND_URL"
echo ""

echo "Testing CORS preflight request..."
echo "-----------------------------------"

# Send an OPTIONS request (CORS preflight)
response=$(curl -s -I -X OPTIONS \
  -H "Origin: $FRONTEND_URL" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: Content-Type" \
  "$BACKEND_URL/api/stats")

echo "$response"
echo ""

# Check for CORS headers
if echo "$response" | grep -qi "access-control-allow-origin"; then
    echo "✅ CORS is configured!"
    echo ""
    echo "CORS Headers:"
    echo "$response" | grep -i "access-control"
else
    echo "❌ CORS is NOT configured properly!"
    echo ""
    echo "🔧 Fix: Add this to Railway Variables:"
    echo "CORS_ORIGINS=$FRONTEND_URL,https://faiz-lab-git-*.vercel.app,https://faiz-lab-*.vercel.app"
fi

echo ""
echo "=============================="


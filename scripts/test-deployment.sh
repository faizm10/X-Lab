#!/bin/bash

echo "🧪 Testing Deployment Connection"
echo "=================================="
echo ""

# Get URLs from user
read -p "Enter your Railway backend URL (e.g., https://xxx.up.railway.app): " BACKEND_URL
read -p "Enter your Vercel frontend URL (e.g., https://xxx.vercel.app): " FRONTEND_URL

echo ""
echo "Testing backend health..."
BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/health")

if [ "$BACKEND_STATUS" -eq 200 ]; then
    echo "✅ Backend is healthy (HTTP $BACKEND_STATUS)"
else
    echo "❌ Backend health check failed (HTTP $BACKEND_STATUS)"
fi

echo ""
echo "Testing backend API stats..."
STATS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/api/stats")

if [ "$STATS_STATUS" -eq 200 ]; then
    echo "✅ Backend API is working (HTTP $STATS_STATUS)"
    echo ""
    echo "Stats response:"
    curl -s "$BACKEND_URL/api/stats" | python3 -m json.tool
else
    echo "❌ Backend API failed (HTTP $STATS_STATUS)"
fi

echo ""
echo "Testing frontend..."
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL")

if [ "$FRONTEND_STATUS" -eq 200 ]; then
    echo "✅ Frontend is accessible (HTTP $FRONTEND_STATUS)"
else
    echo "❌ Frontend failed (HTTP $FRONTEND_STATUS)"
fi

echo ""
echo "Testing CORS (frontend → backend)..."
CORS_TEST=$(curl -s -o /dev/null -w "%{http_code}" -H "Origin: $FRONTEND_URL" "$BACKEND_URL/api/stats")

if [ "$CORS_TEST" -eq 200 ]; then
    echo "✅ CORS is configured correctly"
else
    echo "⚠️  CORS might need adjustment (HTTP $CORS_TEST)"
    echo "Make sure to add '$FRONTEND_URL' to CORS_ORIGINS on Railway"
fi

echo ""
echo "=================================="
echo "✅ Deployment test complete!"
echo ""
echo "Your apps:"
echo "  Frontend: $FRONTEND_URL"
echo "  Backend:  $BACKEND_URL"
echo "  API Docs: $BACKEND_URL/docs"


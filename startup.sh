#!/bin/bash

# ContextBridge Startup Script
# One-command deployment for hackathon demo

set -e  # Exit on error

echo "🚀 Starting ContextBridge..."
echo "================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your GEMINI_API_KEY"
    echo "   Get your key from: https://makersuite.google.com/app/apikey"
    echo ""
    read -p "Press Enter after you've added your API key to .env..."
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running!"
    echo "   Please start Docker Desktop and try again."
    exit 1
fi

echo "📦 Step 1: Building and starting services..."
docker-compose up -d --build

echo ""
echo "⏳ Step 2: Waiting for API to be ready..."
echo "   (This may take 30-60 seconds on first run)"

# Wait for API health check
MAX_RETRIES=30
RETRY_COUNT=0
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
        echo "   ✅ API is ready!"
        break
    fi
    echo -n "."
    sleep 2
    RETRY_COUNT=$((RETRY_COUNT + 1))
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo ""
    echo "❌ API failed to start. Check logs with: docker-compose logs contextbridge-api"
    exit 1
fi

echo ""
echo "📊 Step 3: Seeding demo data..."
SEED_RESPONSE=$(curl -s -X POST http://localhost:8000/api/demo/seed)
echo "   ✅ Demo data loaded!"

echo ""
echo "⏳ Step 4: Waiting for frontend to be ready..."
MAX_RETRIES=20
RETRY_COUNT=0
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo "   ✅ Frontend is ready!"
        break
    fi
    echo -n "."
    sleep 2
    RETRY_COUNT=$((RETRY_COUNT + 1))
done

echo ""
echo "================================"
echo "✅ ContextBridge is running!"
echo "================================"
echo ""
echo "📱 Access the application:"
echo "   🎯 Demo Page:   http://localhost:3000/demo"
echo "   📊 Dashboard:   http://localhost:3000"
echo "   📚 API Docs:    http://localhost:8000/docs"
echo "   ❤️  Health:     http://localhost:8000/api/health"
echo ""
echo "🎭 Hackathon Demo:"
echo "   1. Open http://localhost:3000/demo"
echo "   2. Click 'Scenario A: Prevent a Mistake'"
echo "   3. Watch the magic! ✨"
echo ""
echo "📋 Useful commands:"
echo "   View logs:      docker-compose logs -f"
echo "   Stop services:  docker-compose down"
echo "   Restart:        docker-compose restart"
echo ""
echo "🏆 Good luck with your presentation!"
echo ""

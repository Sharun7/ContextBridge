@echo off
REM ContextBridge Startup Script for Windows
REM One-command deployment for hackathon demo

echo.
echo ================================
echo 🚀 Starting ContextBridge...
echo ================================
echo.

REM Check if .env exists
if not exist .env (
    echo ⚠️  .env file not found!
    echo 📝 Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANT: Please edit .env and add your GEMINI_API_KEY
    echo    Get your key from: https://makersuite.google.com/app/apikey
    echo.
    pause
)

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running!
    echo    Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo 📦 Step 1: Building and starting services...
docker-compose up -d --build

echo.
echo ⏳ Step 2: Waiting for API to be ready...
echo    (This may take 30-60 seconds on first run)

REM Wait for API health check
set MAX_RETRIES=30
set RETRY_COUNT=0

:wait_api
if %RETRY_COUNT% geq %MAX_RETRIES% (
    echo.
    echo ❌ API failed to start. Check logs with: docker-compose logs contextbridge-api
    pause
    exit /b 1
)

curl -s http://localhost:8000/api/health >nul 2>&1
if errorlevel 1 (
    echo|set /p="."
    timeout /t 2 /nobreak >nul
    set /a RETRY_COUNT+=1
    goto wait_api
)

echo    ✅ API is ready!

echo.
echo 📊 Step 3: Seeding demo data...
curl -s -X POST http://localhost:8000/api/demo/seed >nul
echo    ✅ Demo data loaded!

echo.
echo ⏳ Step 4: Waiting for frontend to be ready...
set MAX_RETRIES=20
set RETRY_COUNT=0

:wait_frontend
if %RETRY_COUNT% geq %MAX_RETRIES% (
    echo.
    echo ⚠️  Frontend may still be starting...
    goto show_urls
)

curl -s http://localhost:3000 >nul 2>&1
if errorlevel 1 (
    echo|set /p="."
    timeout /t 2 /nobreak >nul
    set /a RETRY_COUNT+=1
    goto wait_frontend
)

echo    ✅ Frontend is ready!

:show_urls
echo.
echo ================================
echo ✅ ContextBridge is running!
echo ================================
echo.
echo 📱 Access the application:
echo    🎯 Demo Page:   http://localhost:3000/demo
echo    📊 Dashboard:   http://localhost:3000
echo    📚 API Docs:    http://localhost:8000/docs
echo    ❤️  Health:     http://localhost:8000/api/health
echo.
echo 🎭 Hackathon Demo:
echo    1. Open http://localhost:3000/demo
echo    2. Click 'Scenario A: Prevent a Mistake'
echo    3. Watch the magic! ✨
echo.
echo 📋 Useful commands:
echo    View logs:      docker-compose logs -f
echo    Stop services:  docker-compose down
echo    Restart:        docker-compose restart
echo.
echo 🏆 Good luck with your presentation!
echo.

REM Open browser automatically
start http://localhost:3000/demo

pause

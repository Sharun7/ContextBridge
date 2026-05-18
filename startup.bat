@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ContextBridge Startup Script for Windows
REM Uses Docker when available, otherwise falls back to the local Node runtime API.

set "ROOT_DIR=%~dp0"
if "%ROOT_DIR:~-1%"=="\" set "ROOT_DIR=%ROOT_DIR:~0,-1%"
set "FRONTEND_DIR=%ROOT_DIR%\frontend"

echo.
echo ================================
echo Starting ContextBridge...
echo ================================
echo.

if not exist "%ROOT_DIR%\.env" (
    echo .env file not found.
    echo Creating .env from .env.example...
    copy "%ROOT_DIR%\.env.example" "%ROOT_DIR%\.env" >nul
    echo.
    echo IMPORTANT: Please update .env with your GEMINI_API_KEY if you want live model output.
    echo Demo mode can still run with the local runtime dataset.
    echo.
)

call :check_endpoint "http://127.0.0.1:8000/api/health"
if "!ERRORLEVEL!"=="0" (
    echo Backend already responding on port 8000.
) else (
    docker info >nul 2>&1
    if "!ERRORLEVEL!"=="0" (
        echo Docker is available. Starting containerized services...
        pushd "%ROOT_DIR%"
        docker-compose up -d --build
        popd
    ) else (
        echo Docker is not available. Falling back to local runtime mode...
        call :start_local_backend
    )
)

echo.
echo Waiting for backend health check...
call :wait_for_endpoint "http://127.0.0.1:8000/api/health" 40 "Backend failed to start."
if errorlevel 1 goto :fail
echo Backend is ready.

echo.
echo Seeding knowledge data...
powershell -NoProfile -ExecutionPolicy Bypass -Command "try { Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:8000/api/demo/seed' -Method POST | Out-Null; exit 0 } catch { exit 1 }"
if errorlevel 1 (
    echo Demo seed request failed. Continuing anyway.
) else (
    echo Knowledge data is loaded.
)

call :check_endpoint "http://127.0.0.1:3000/"
if "!ERRORLEVEL!"=="0" (
    echo Frontend already responding on port 3000.
) else (
    call :start_frontend
)

echo.
echo Waiting for frontend...
call :wait_for_endpoint "http://127.0.0.1:3000/" 40 "Frontend failed to start."
if errorlevel 1 goto :fail
echo Frontend is ready.

echo.
echo ================================
echo ContextBridge is running
echo ================================
echo.
echo Dashboard:   http://localhost:3000/
echo Knowledge:   http://localhost:3000/knowledge
echo Ask Context: http://localhost:3000/query
echo Graph:       http://localhost:3000/graph
echo Demo:        http://localhost:3000/demo
echo Health:      http://localhost:8000/api/health
echo.
echo Note: If Docker was unavailable, the backend is running on the local Node runtime fallback.
echo.

start "" "http://localhost:3000/"
goto :eof

:start_local_backend
where node >nul 2>&1
if errorlevel 1 (
    echo Node.js is required for the local runtime fallback but was not found.
    exit /b 1
)

echo Starting local runtime backend...
start "ContextBridge Backend" /min cmd /c "cd /d ""%ROOT_DIR%"" && node local_runtime_api.js"
exit /b 0

:start_frontend
where npm >nul 2>&1
if errorlevel 1 (
    echo npm is required to start the frontend but was not found.
    exit /b 1
)

echo Starting frontend dev server...
start "ContextBridge Frontend" /min cmd /c "cd /d ""%FRONTEND_DIR%"" && npm start"
exit /b 0

:check_endpoint
powershell -NoProfile -ExecutionPolicy Bypass -Command "try { $r = Invoke-WebRequest -UseBasicParsing -Uri '%~1' -TimeoutSec 5; if ($r.StatusCode -ge 200 -and $r.StatusCode -lt 500) { exit 0 } else { exit 1 } } catch { exit 1 }"
exit /b %ERRORLEVEL%

:wait_for_endpoint
set "WAIT_URL=%~1"
set "WAIT_RETRIES=%~2"
set "WAIT_ERROR=%~3"
set /a WAIT_COUNT=0

:wait_loop
call :check_endpoint "%WAIT_URL%"
if "!ERRORLEVEL!"=="0" exit /b 0

if "!WAIT_COUNT!" geq "!WAIT_RETRIES!" (
    echo %WAIT_ERROR%
    exit /b 1
)

set /a WAIT_COUNT+=1
timeout /t 2 /nobreak >nul
goto :wait_loop

:fail
echo.
echo ContextBridge could not be started automatically.
echo Check the backend and frontend terminals for the first failing step.
exit /b 1

#!/bin/bash

# ContextBridge Startup Script
# Uses Docker when available, otherwise falls back to the local Node runtime API.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
FRONTEND_DIR="$ROOT_DIR/frontend"

echo "================================"
echo "Starting ContextBridge..."
echo "================================"
echo

if [ ! -f "$ROOT_DIR/.env" ]; then
  echo ".env file not found."
  echo "Creating .env from .env.example..."
  cp "$ROOT_DIR/.env.example" "$ROOT_DIR/.env"
  echo
  echo "IMPORTANT: Please update .env with your GEMINI_API_KEY if you want live model output."
  echo "Demo mode can still run with the local runtime dataset."
  echo
fi

check_endpoint() {
  curl -fsS "$1" >/dev/null 2>&1
}

wait_for_endpoint() {
  local url="$1"
  local retries="$2"
  local error_message="$3"
  local count=0

  until check_endpoint "$url"; do
    if [ "$count" -ge "$retries" ]; then
      echo "$error_message"
      return 1
    fi
    count=$((count + 1))
    sleep 2
  done
}

start_local_backend() {
  if ! command -v node >/dev/null 2>&1; then
    echo "Node.js is required for the local runtime fallback but was not found."
    return 1
  fi

  echo "Starting local runtime backend..."
  (
    cd "$ROOT_DIR"
    nohup node local_runtime_api.js >/tmp/contextbridge-backend.log 2>&1 &
  )
}

start_frontend() {
  if ! command -v npm >/dev/null 2>&1; then
    echo "npm is required to start the frontend but was not found."
    return 1
  fi

  echo "Starting frontend dev server..."
  (
    cd "$FRONTEND_DIR"
    nohup npm start >/tmp/contextbridge-frontend.log 2>&1 &
  )
}

if check_endpoint "http://127.0.0.1:8000/api/health"; then
  echo "Backend already responding on port 8000."
else
  if docker info >/dev/null 2>&1; then
    echo "Docker is available. Starting containerized services..."
    (
      cd "$ROOT_DIR"
      docker-compose up -d --build
    )
  else
    echo "Docker is not available. Falling back to local runtime mode..."
    start_local_backend
  fi
fi

echo
echo "Waiting for backend health check..."
wait_for_endpoint "http://127.0.0.1:8000/api/health" 40 "Backend failed to start."
echo "Backend is ready."

echo
echo "Seeding knowledge data..."
if curl -fsS -X POST "http://127.0.0.1:8000/api/demo/seed" >/dev/null 2>&1; then
  echo "Knowledge data is loaded."
else
  echo "Demo seed request failed. Continuing anyway."
fi

if check_endpoint "http://127.0.0.1:3000/"; then
  echo "Frontend already responding on port 3000."
else
  start_frontend
fi

echo
echo "Waiting for frontend..."
wait_for_endpoint "http://127.0.0.1:3000/" 40 "Frontend failed to start."
echo "Frontend is ready."

echo
echo "================================"
echo "ContextBridge is running"
echo "================================"
echo
echo "Dashboard:   http://localhost:3000/"
echo "Knowledge:   http://localhost:3000/knowledge"
echo "Ask Context: http://localhost:3000/query"
echo "Graph:       http://localhost:3000/graph"
echo "Demo:        http://localhost:3000/demo"
echo "Health:      http://localhost:8000/api/health"
echo
echo "Note: If Docker was unavailable, the backend is running on the local Node runtime fallback."

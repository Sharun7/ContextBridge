"""
ContextBridge - AI-Powered Institutional Memory Agent
FastAPI Application Entry Point
"""

import logging
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings, ensure_directories
from api.routes import router
from db.database import init_db

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("🚀 Starting ContextBridge...")
    ensure_directories()
    init_db()
    logger.info("✅ ContextBridge initialized successfully")
    logger.info(f"📊 Demo Mode: {settings.DEMO_MODE}")
    logger.info(f"🔑 Gemini API Key: {'Configured' if settings.GEMINI_API_KEY else 'Missing'}")
    
    yield
    
    # Shutdown
    logger.info("👋 Shutting down ContextBridge...")


# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all API requests"""
    start_time = time.time()
    
    # Log request
    logger.info(f"→ {request.method} {request.url.path}")
    
    # Process request
    response = await call_next(request)
    
    # Log response
    duration = time.time() - start_time
    logger.info(f"← {request.method} {request.url.path} - {response.status_code} ({duration:.2f}s)")
    
    return response


# Include API routes
app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "ContextBridge",
        "version": settings.API_VERSION,
        "description": "AI-Powered Institutional Memory Agent for Enterprises",
        "status": "running",
        "demo_mode": settings.DEMO_MODE,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "demo_mode": settings.DEMO_MODE,
        "gemini_configured": bool(settings.GEMINI_API_KEY)
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD
    )

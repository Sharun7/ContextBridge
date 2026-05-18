"""
ContextBridge Configuration Module
Loads environment variables and application settings
"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Gemini AI Configuration
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"
    
    # Vector Store Configuration
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "contextbridge_knowledge"
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./contextbridge.db"
    
    # Demo Mode
    DEMO_MODE: bool = True
    
    # Slack Configuration
    SLACK_BOT_TOKEN: Optional[str] = None
    SLACK_APP_TOKEN: Optional[str] = None
    
    # Jira Configuration
    JIRA_URL: Optional[str] = None
    JIRA_EMAIL: Optional[str] = None
    JIRA_API_TOKEN: Optional[str] = None
    
    # Google Drive Configuration
    GOOGLE_DRIVE_CREDENTIALS_PATH: Optional[str] = None
    GOOGLE_DRIVE_SERVICE_ACCOUNT_PATH: Optional[str] = None
    
    # Gmail Configuration
    GMAIL_CREDENTIALS_PATH: Optional[str] = None
    GMAIL_SERVICE_ACCOUNT_PATH: Optional[str] = None
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = int(os.getenv("PORT", "8000"))
    API_RELOAD: bool = os.getenv("ENVIRONMENT", "development") != "production"
    API_TITLE: str = "ContextBridge API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "AI-Powered Institutional Memory Agent for Enterprises"
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # CORS Configuration
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",")
    
    # Knowledge Extraction Settings
    EXTRACTION_BATCH_SIZE: int = 10
    EXTRACTION_DELAY_MS: int = 500
    
    # Proactive Alert Settings
    ALERT_CONFIDENCE_THRESHOLD: int = 60
    ALERT_MIN_IMPORTANCE_SCORE: int = 6
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings"""
    return settings


def ensure_directories():
    """Ensure required directories exist"""
    Path(settings.CHROMA_PERSIST_DIR).mkdir(parents=True, exist_ok=True)
    Path("demo/data").mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(parents=True, exist_ok=True)


# Initialize directories on import
ensure_directories()

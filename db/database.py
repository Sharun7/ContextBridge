"""
Database Module
SQLite for audit logs and metadata storage
"""

import logging
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings

logger = logging.getLogger(__name__)

Base = declarative_base()


class AuditLog(Base):
    """Audit log for all system actions"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    action_type = Column(String(50), nullable=False)  # ingest, query, alert, etc.
    user_id = Column(String(100))
    details = Column(Text)
    success = Column(Boolean, default=True)


class KnowledgeMetadata(Base):
    """Metadata for knowledge items"""
    __tablename__ = "knowledge_metadata"
    
    id = Column(String(100), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    source_type = Column(String(50), nullable=False)
    source_id = Column(String(200), nullable=False)
    content_type = Column(String(50))
    importance_score = Column(Integer)
    access_count = Column(Integer, default=0)


class AlertHistory(Base):
    """History of proactive alerts"""
    __tablename__ = "alert_history"
    
    id = Column(String(100), primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    trigger_type = Column(String(50), nullable=False)
    alert_level = Column(String(20))
    confidence_score = Column(Integer)
    user_id = Column(String(100))
    was_helpful = Column(Boolean)


# Database engine and session
engine = None
SessionLocal = None


def init_db():
    """Initialize database"""
    global engine, SessionLocal
    
    try:
        engine = create_engine(
            settings.DATABASE_URL,
            connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
        )
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Create session factory
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        logger.info("✅ Database initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise


def get_db():
    """Get database session"""
    if SessionLocal is None:
        init_db()
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def log_action(action_type: str, user_id: str = None, details: str = None, success: bool = True):
    """Log an action to audit log"""
    try:
        db = SessionLocal()
        log = AuditLog(
            action_type=action_type,
            user_id=user_id,
            details=details,
            success=success
        )
        db.add(log)
        db.commit()
        db.close()
    except Exception as e:
        logger.error(f"Failed to log action: {e}")

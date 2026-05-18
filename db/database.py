"""
Database helpers backed by sqlite3 from the Python standard library.

This keeps the local app runnable without SQLAlchemy while preserving the
existing public functions used by the FastAPI app.
"""

import logging
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

from config import settings

logger = logging.getLogger(__name__)

DB_PATH = Path(settings.DATABASE_URL.replace("sqlite:///", ""))


def init_db():
    """Initialize sqlite tables used by the app."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
                action_type TEXT NOT NULL,
                user_id TEXT,
                details TEXT,
                success INTEGER DEFAULT 1
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS knowledge_metadata (
                id TEXT PRIMARY KEY,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                source_type TEXT NOT NULL,
                source_id TEXT NOT NULL,
                content_type TEXT,
                importance_score INTEGER,
                access_count INTEGER DEFAULT 0
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS alert_history (
                id TEXT PRIMARY KEY,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
                trigger_type TEXT NOT NULL,
                alert_level TEXT,
                confidence_score INTEGER,
                user_id TEXT,
                was_helpful INTEGER
            )
            """
        )
        connection.commit()

    logger.info("✅ Database initialized successfully")


@contextmanager
def get_db() -> Iterator[sqlite3.Connection]:
    """Yield a sqlite connection for compatibility."""
    connection = sqlite3.connect(DB_PATH)
    try:
        yield connection
    finally:
        connection.close()


def log_action(
    action_type: str,
    user_id: Optional[str] = None,
    details: Optional[str] = None,
    success: bool = True,
):
    """Write a simple audit log row."""
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO audit_logs (action_type, user_id, details, success)
                VALUES (?, ?, ?, ?)
                """,
                (action_type, user_id, details, 1 if success else 0),
            )
            connection.commit()
    except Exception as exc:
        logger.error("Failed to log action: %s", exc)

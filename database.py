"""
database.py — SQLite-backed persistence layer for the Fitness Bot.

Tables
------
progress : stores user workout logs
"""

import sqlite3
import logging
from datetime import datetime

DB_PATH = "fitness_bot.db"
logger = logging.getLogger(__name__)


def get_connection() -> sqlite3.Connection:
    """Return a SQLite connection with row_factory set."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables if they don't exist yet."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS progress (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id   INTEGER NOT NULL,
                date      TEXT    NOT NULL,
                exercise  TEXT    NOT NULL,
                sets      INTEGER,
                reps      INTEGER,
                weight_kg REAL,
                notes     TEXT
            )
            """
        )
        conn.commit()
    logger.info("Database initialised.")


def insert_log(
    user_id: int,
    exercise: str,
    sets: int,
    reps: int,
    weight_kg: float,
    notes: str = "",
) -> None:
    """Insert a new progress log entry for a user."""
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO progress (user_id, date, exercise, sets, reps, weight_kg, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, date_str, exercise, sets, reps, weight_kg, notes),
        )
        conn.commit()


def fetch_logs(user_id: int, limit: int = 10) -> list[sqlite3.Row]:
    """Fetch the most recent progress logs for a user."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT date, exercise, sets, reps, weight_kg, notes
            FROM progress
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
    return rows


# Initialise the DB on import
init_db()

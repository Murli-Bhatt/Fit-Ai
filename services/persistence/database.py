"""
database.py
-----------
SQLite3 connection manager for FIT-AI Gym Trainer.
Handles DB file path, connection creation, and schema initialisation.
"""

import sqlite3
import os
from pathlib import Path

# ── DB file lives at project root / data / data.db ───────────────────────────
_BASE_DIR = Path(__file__).resolve().parent.parent.parent   # project root
_DB_DIR   = _BASE_DIR / "data"
DB_PATH   = _DB_DIR / "data.db"


def get_connection() -> sqlite3.Connection:
    """
    Return a new SQLite connection with:
      - Row factory so rows behave like dicts
      - Foreign-key enforcement enabled
    """
    _DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """
    Create all tables if they do not already exist.

    Schema
    ──────
    users
        user_id       INTEGER  PRIMARY KEY AUTOINCREMENT
        username      TEXT     UNIQUE  NOT NULL
        email         TEXT     UNIQUE  NOT NULL
        password_hash TEXT     NOT NULL
        created_at    TEXT     NOT NULL  (ISO-8601 datetime)

    exercise_logs
        log_id          INTEGER  PRIMARY KEY AUTOINCREMENT
        user_id         INTEGER  NOT NULL  REFERENCES users(user_id)
        exercise_name   TEXT     NOT NULL
        total_reps      INTEGER  NOT NULL  DEFAULT 0
        total_sets      INTEGER  NOT NULL  DEFAULT 0
        target_reps     INTEGER  NOT NULL  DEFAULT 0
        target_sets     INTEGER  NOT NULL  DEFAULT 0
        log_date        TEXT     NOT NULL  (YYYY-MM-DD)
        last_updated_at TEXT     NOT NULL  (ISO-8601 datetime)

    Unique constraint on (user_id, exercise_name, log_date) enforces the
    "same exercise on same day → update, different day → new row" rule.
    """
    conn = get_connection()
    try:
        cur = conn.cursor()

        # ── users ─────────────────────────────────────────────────────────────
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id       INTEGER PRIMARY KEY AUTOINCREMENT,
                username      TEXT    NOT NULL UNIQUE COLLATE NOCASE,
                email         TEXT    NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT    NOT NULL,
                created_at    TEXT    NOT NULL
            )
        """)

        # ── exercise_logs ─────────────────────────────────────────────────────
        cur.execute("""
            CREATE TABLE IF NOT EXISTS exercise_logs (
                log_id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id         INTEGER NOT NULL,
                exercise_name   TEXT    NOT NULL,
                total_reps      INTEGER NOT NULL DEFAULT 0,
                total_sets      INTEGER NOT NULL DEFAULT 0,
                target_reps     INTEGER NOT NULL DEFAULT 0,
                target_sets     INTEGER NOT NULL DEFAULT 0,
                log_date        TEXT    NOT NULL,
                last_updated_at TEXT    NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                UNIQUE (user_id, exercise_name, log_date)
            )
        """)

        conn.commit()
    finally:
        conn.close()

"""
user_repository.py
------------------
All database operations related to the users table.

Functions
---------
register_user(username, email, password)  -> (bool, str)
authenticate_user(username, password)     -> (bool, int | None)
get_user_by_username(username)            -> dict | None
user_exists(username)                     -> bool
email_exists(email)                       -> bool
"""

import hashlib
import datetime
from services.persistence.database import get_connection


# ── Helpers ───────────────────────────────────────────────────────────────────

def _hash_password(password: str) -> str:
    """SHA-256 hash of the password string."""
    return hashlib.sha256(password.strip().encode("utf-8")).hexdigest()


def _now_iso() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ── Public API ────────────────────────────────────────────────────────────────

def user_exists(username: str) -> bool:
    """Return True if a user with this username already exists (case-insensitive)."""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT 1 FROM users WHERE username = ? COLLATE NOCASE",
            (username.strip(),)
        ).fetchone()
        return row is not None
    finally:
        conn.close()


def email_exists(email: str) -> bool:
    """Return True if this email is already registered (case-insensitive)."""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT 1 FROM users WHERE email = ? COLLATE NOCASE",
            (email.strip(),)
        ).fetchone()
        return row is not None
    finally:
        conn.close()


def register_user(username: str, email: str, password: str) -> tuple[bool, str]:
    """
    Register a new user.

    Returns
    -------
    (True,  "Account created successfully!")  on success
    (False, <reason string>)                  on failure
    """
    username = username.strip()
    email    = email.strip()

    if not username or not email or not password:
        return False, "All fields are required."

    if user_exists(username):
        return False, "Username already exists. Please choose a different one."

    if email_exists(email):
        return False, "An account with this email already exists."

    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO users (username, email, password_hash, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (username, email, _hash_password(password), _now_iso())
        )
        conn.commit()
        return True, "Account created successfully!"
    except Exception as exc:
        return False, f"Registration failed: {exc}"
    finally:
        conn.close()


def authenticate_user(username: str, password: str) -> tuple[bool, int | None]:
    """
    Verify credentials against the database.

    Returns
    -------
    (True,  user_id)  if credentials are valid
    (False, None)     if username not found or password wrong
    """
    username = username.strip()
    if not username or not password:
        return False, None

    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT user_id, password_hash FROM users WHERE username = ? COLLATE NOCASE",
            (username,)
        ).fetchone()

        if row is None:
            return False, None   # user not found

        if row["password_hash"] != _hash_password(password):
            return False, None   # wrong password

        return True, row["user_id"]
    finally:
        conn.close()


def get_user_by_username(username: str) -> dict | None:
    """
    Fetch full user record by username.

    Returns a dict with keys: user_id, username, email, created_at
    or None if not found.
    """
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT user_id, username, email, created_at FROM users WHERE username = ? COLLATE NOCASE",
            (username.strip(),)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_user_by_id(user_id: int) -> dict | None:
    """Fetch user record by primary key."""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT user_id, username, email, created_at FROM users WHERE user_id = ?",
            (user_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

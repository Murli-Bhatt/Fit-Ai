"""
exercise_repository.py
----------------------
All database operations related to the exercise_logs table.

Key rule
--------
Same user + same exercise + same calendar date  →  UPDATE (aggregate reps/sets)
Same user + same exercise + different date       →  INSERT new row

Functions
---------
save_workout_log(user_id, exercise_name, total_reps, total_sets,
                 target_reps, target_sets)          -> None

get_logs_for_user(user_id)                          -> list[dict]
get_logs_for_user_by_exercise(user_id, exercise)    -> list[dict]
get_logs_for_user_by_date_range(user_id, start, end)-> list[dict]
get_exercise_summary(user_id)                       -> list[dict]
get_today_log(user_id, exercise_name)               -> dict | None
"""

import datetime
from services.persistence.database import get_connection


# ── Helpers ───────────────────────────────────────────────────────────────────

def _today() -> str:
    return datetime.date.today().strftime("%Y-%m-%d")


def _now_iso() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ── Public API ────────────────────────────────────────────────────────────────

def save_workout_log(
    user_id:       int,
    exercise_name: str,
    total_reps:    int,
    total_sets:    int,
    target_reps:   int,
    target_sets:   int,
) -> None:
    """
    Persist a completed workout session.

    Logic
    -----
    1. Check if a row already exists for (user_id, exercise_name, today).
    2. If YES  → UPDATE: add reps/sets to existing totals (aggregation).
    3. If NO   → INSERT: create a fresh row for today.

    Edge cases handled
    ------------------
    - total_reps <= 0 : skip saving (nothing was done)
    - user_id is None : skip saving (not logged in properly)
    """
    if not user_id or total_reps <= 0:
        return

    today    = _today()
    now      = _now_iso()
    conn     = get_connection()

    try:
        existing = conn.execute(
            """
            SELECT log_id, total_reps, total_sets
            FROM   exercise_logs
            WHERE  user_id = ? AND exercise_name = ? AND log_date = ?
            """,
            (user_id, exercise_name, today)
        ).fetchone()

        if existing:
            # ── Same exercise, same day → aggregate ──────────────────────────
            conn.execute(
                """
                UPDATE exercise_logs
                SET    total_reps      = total_reps + ?,
                       total_sets      = total_sets + ?,
                       target_reps     = ?,
                       target_sets     = ?,
                       last_updated_at = ?
                WHERE  log_id = ?
                """,
                (total_reps, total_sets, target_reps, target_sets, now, existing["log_id"])
            )
        else:
            # ── New day or first time for this exercise → insert ──────────────
            conn.execute(
                """
                INSERT INTO exercise_logs
                    (user_id, exercise_name, total_reps, total_sets,
                     target_reps, target_sets, log_date, last_updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (user_id, exercise_name, total_reps, total_sets,
                 target_reps, target_sets, today, now)
            )

        conn.commit()
    finally:
        conn.close()


def get_logs_for_user(user_id: int) -> list[dict]:
    """
    Return all exercise logs for a user, newest first.

    Each dict has:
        log_id, exercise_name, total_reps, total_sets,
        target_reps, target_sets, log_date, last_updated_at
    """
    if not user_id:
        return []

    conn = get_connection()
    try:
        rows = conn.execute(
            """
            SELECT log_id, exercise_name, total_reps, total_sets,
                   target_reps, target_sets, log_date, last_updated_at
            FROM   exercise_logs
            WHERE  user_id = ?
            ORDER  BY log_date DESC, last_updated_at DESC
            """,
            (user_id,)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_logs_for_user_by_exercise(user_id: int, exercise_name: str) -> list[dict]:
    """Return logs filtered by a specific exercise, newest first."""
    if not user_id:
        return []

    conn = get_connection()
    try:
        rows = conn.execute(
            """
            SELECT log_id, exercise_name, total_reps, total_sets,
                   target_reps, target_sets, log_date, last_updated_at
            FROM   exercise_logs
            WHERE  user_id = ? AND exercise_name = ?
            ORDER  BY log_date DESC
            """,
            (user_id, exercise_name)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_logs_for_user_by_date_range(
    user_id:    int,
    start_date: str,   # "YYYY-MM-DD"
    end_date:   str,   # "YYYY-MM-DD"
) -> list[dict]:
    """Return logs within an inclusive date range, newest first."""
    if not user_id:
        return []

    conn = get_connection()
    try:
        rows = conn.execute(
            """
            SELECT log_id, exercise_name, total_reps, total_sets,
                   target_reps, target_sets, log_date, last_updated_at
            FROM   exercise_logs
            WHERE  user_id = ?
              AND  log_date BETWEEN ? AND ?
            ORDER  BY log_date DESC, exercise_name
            """,
            (user_id, start_date, end_date)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_exercise_summary(user_id: int) -> list[dict]:
    """
    Aggregate stats per exercise across all time for a user.

    Returns list of dicts with:
        exercise_name, total_sessions, lifetime_reps,
        lifetime_sets, first_session, last_session
    """
    if not user_id:
        return []

    conn = get_connection()
    try:
        rows = conn.execute(
            """
            SELECT exercise_name,
                   COUNT(*)        AS total_sessions,
                   SUM(total_reps) AS lifetime_reps,
                   SUM(total_sets) AS lifetime_sets,
                   MIN(log_date)   AS first_session,
                   MAX(log_date)   AS last_session
            FROM   exercise_logs
            WHERE  user_id = ?
            GROUP  BY exercise_name
            ORDER  BY lifetime_reps DESC
            """,
            (user_id,)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_today_log(user_id: int, exercise_name: str) -> dict | None:
    """
    Return today's log row for a specific exercise, or None if not found.
    Useful for showing the user what they've already done today.
    """
    if not user_id:
        return None

    conn = get_connection()
    try:
        row = conn.execute(
            """
            SELECT log_id, exercise_name, total_reps, total_sets,
                   target_reps, target_sets, log_date, last_updated_at
            FROM   exercise_logs
            WHERE  user_id = ? AND exercise_name = ? AND log_date = ?
            """,
            (user_id, exercise_name, _today())
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

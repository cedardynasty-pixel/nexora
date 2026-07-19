"""
db.py — SQLite persistence layer for Nexora.

Handles user accounts. Passwords are stored as PBKDF2-HMAC-SHA256 hashes
with a per-user random salt (never store plaintext passwords).
"""

import sqlite3
import hashlib
import os
import secrets
from datetime import datetime
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "nexora.db")


def _hash_password(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000).hex()


@contextmanager
def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL,
                grade TEXT,
                salt BLOB NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS enrollments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                subject TEXT NOT NULL,
                progress INTEGER DEFAULT 0,
                UNIQUE(username, subject)
            )
            """
        )


def username_exists(username: str) -> bool:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT 1 FROM users WHERE username = ?", (username,)
        ).fetchone()
        return row is not None


def create_user(username: str, email: str, password: str, grade: str) -> tuple[bool, str]:
    if not username or not password:
        return False, "Username and password are required."
    if username_exists(username):
        return False, "That username is already taken."

    salt = secrets.token_bytes(16)
    pwd_hash = _hash_password(password, salt)

    with get_conn() as conn:
        conn.execute(
            "INSERT INTO users (username, email, grade, salt, password_hash, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (username, email, grade, salt, pwd_hash, datetime.utcnow().isoformat()),
        )
        # seed a couple of default enrollments so the dashboard has something to show
        for subject, progress in [("Mathematics", 0), ("Science", 0)]:
            conn.execute(
                "INSERT OR IGNORE INTO enrollments (username, subject, progress) VALUES (?, ?, ?)",
                (username, subject, progress),
            )
    return True, "Account created successfully."


def verify_user(username: str, password: str) -> tuple[bool, str]:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
    if row is None:
        return False, "No account found with that username."

    candidate_hash = _hash_password(password, row["salt"])
    if secrets.compare_digest(candidate_hash, row["password_hash"]):
        return True, "Login successful."
    return False, "Incorrect password."


def get_user(username: str) -> sqlite3.Row | None:
    with get_conn() as conn:
        return conn.execute(
            "SELECT id, username, email, grade, created_at FROM users WHERE username = ?",
            (username,),
        ).fetchone()


def get_enrollments(username: str):
    with get_conn() as conn:
        return conn.execute(
            "SELECT subject, progress FROM enrollments WHERE username = ?", (username,)
        ).fetchall()


def update_progress(username: str, subject: str, progress: int):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO enrollments (username, subject, progress) VALUES (?, ?, ?) "
            "ON CONFLICT(username, subject) DO UPDATE SET progress = excluded.progress",
            (username, subject, progress),
        )

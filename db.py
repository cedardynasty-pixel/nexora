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
                created_at TEXT NOT NULL,
                is_admin INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        # keep old databases (created before this column existed) working
        existing_cols = [row["name"] for row in conn.execute("PRAGMA table_info(users)")]
        if "is_admin" not in existing_cols:
            conn.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER NOT NULL DEFAULT 0")
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
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                created_by TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS chapters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                order_index INTEGER NOT NULL,
                content TEXT NOT NULL,
                uploaded_by TEXT,
                uploaded_at TEXT NOT NULL,
                FOREIGN KEY (book_id) REFERENCES books(id)
            )
            """
        )


def username_exists(username: str) -> bool:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT 1 FROM users WHERE username = ?", (username,)
        ).fetchone()
        return row is not None


def create_user(username: str, email: str, password: str, grade: str, is_admin: bool = False) -> tuple[bool, str]:
    if not username or not password:
        return False, "Username and password are required."
    if username_exists(username):
        return False, "That username is already taken."

    salt = secrets.token_bytes(16)
    pwd_hash = _hash_password(password, salt)

    with get_conn() as conn:
        conn.execute(
            "INSERT INTO users (username, email, grade, salt, password_hash, created_at, is_admin) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (username, email, grade, salt, pwd_hash, datetime.utcnow().isoformat(), int(is_admin)),
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
            "SELECT id, username, email, grade, created_at, is_admin FROM users WHERE username = ?",
            (username,),
        ).fetchone()


def is_admin_user(username: str) -> bool:
    user = get_user(username)
    return bool(user and user["is_admin"])


def get_all_users():
    with get_conn() as conn:
        return conn.execute(
            "SELECT id, username, email, grade, created_at, is_admin FROM users ORDER BY created_at DESC"
        ).fetchall()


def set_admin(username: str, is_admin: bool):
    with get_conn() as conn:
        conn.execute(
            "UPDATE users SET is_admin = ? WHERE username = ?", (int(is_admin), username)
        )


def delete_user(username: str):
    with get_conn() as conn:
        conn.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.execute("DELETE FROM enrollments WHERE username = ?", (username,))


def any_admin_exists() -> bool:
    with get_conn() as conn:
        row = conn.execute("SELECT 1 FROM users WHERE is_admin = 1 LIMIT 1").fetchone()
        return row is not None


def seed_default_admin(username: str, email: str, password: str, grade: str = "Staff"):
    """Create a first admin account if no admin exists yet. Safe to call on every startup."""
    if any_admin_exists() or username_exists(username):
        return
    create_user(username, email, password, grade, is_admin=True)


def set_password(username: str, new_password: str):
    salt = secrets.token_bytes(16)
    pwd_hash = _hash_password(new_password, salt)
    with get_conn() as conn:
        conn.execute(
            "UPDATE users SET salt = ?, password_hash = ? WHERE username = ?",
            (salt, pwd_hash, username),
        )


def get_setting(key: str) -> str | None:
    with get_conn() as conn:
        row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else None


def set_setting(key: str, value: str):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, value),
        )


def create_book(title: str, created_by: str) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO books (title, created_by, created_at) VALUES (?, ?, ?)",
            (title, created_by, datetime.utcnow().isoformat()),
        )
        return cur.lastrowid


def get_all_books():
    with get_conn() as conn:
        return conn.execute(
            """
            SELECT b.id, b.title, b.created_by, b.created_at,
                   COUNT(c.id) as chapter_count
            FROM books b
            LEFT JOIN chapters c ON c.book_id = b.id
            GROUP BY b.id
            ORDER BY b.created_at DESC
            """
        ).fetchall()


def get_book(book_id: int):
    with get_conn() as conn:
        return conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()


def delete_book(book_id: int):
    with get_conn() as conn:
        conn.execute("DELETE FROM chapters WHERE book_id = ?", (book_id,))
        conn.execute("DELETE FROM books WHERE id = ?", (book_id,))


def add_chapter(book_id: int, title: str, content: str, uploaded_by: str) -> int:
    with get_conn() as conn:
        next_order = conn.execute(
            "SELECT COALESCE(MAX(order_index), 0) + 1 FROM chapters WHERE book_id = ?", (book_id,)
        ).fetchone()[0]
        cur = conn.execute(
            "INSERT INTO chapters (book_id, title, order_index, content, uploaded_by, uploaded_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (book_id, title, next_order, content, uploaded_by, datetime.utcnow().isoformat()),
        )
        return cur.lastrowid


def get_chapters(book_id: int):
    with get_conn() as conn:
        return conn.execute(
            "SELECT id, book_id, title, order_index, uploaded_at, LENGTH(content) as content_len "
            "FROM chapters WHERE book_id = ? ORDER BY order_index",
            (book_id,),
        ).fetchall()


def get_chapter(chapter_id: int):
    with get_conn() as conn:
        return conn.execute("SELECT * FROM chapters WHERE id = ?", (chapter_id,)).fetchone()


def delete_chapter(chapter_id: int):
    with get_conn() as conn:
        conn.execute("DELETE FROM chapters WHERE id = ?", (chapter_id,))


def get_book_full_text(book_id: int) -> str:
    """Concatenate every chapter's content, in order, for whole-book context."""
    chapters = get_chapters(book_id)
    with get_conn() as conn:
        parts = []
        for ch in chapters:
            row = conn.execute("SELECT title, content FROM chapters WHERE id = ?", (ch["id"],)).fetchone()
            parts.append(f"## {row['title']}\n\n{row['content']}")
        return "\n\n".join(parts)


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

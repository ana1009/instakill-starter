"""SQLite bootstrap for InstaKill. Uses the stdlib sqlite3 module (see R11)."""
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Set

DB_PATH = Path(__file__).resolve().parent.parent.parent / "instakill.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES user(id),
    content TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def check_user_exists(user_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM user WHERE id = ?", (user_id,))
        return cursor.fetchone() is not None

def get_user_liked_post_ids(user_id: int) -> set[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT post_id FROM user_like WHERE user_id = ?", (user_id,))
        return {row[0] for row in cursor.fetchall()}

def get_user_followed_authors(user_id: int) -> set[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT followed_id FROM user_follow WHERE follower_id = ?", (user_id,))
        return {row[0] for row in cursor.fetchall()}


def get_feed_candidates() -> list[dict]:
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Modificare aici: convertim created_at în secunde UNIX
        cursor.execute("""
            SELECT id as post_id, user_id, content, 
            COALESCE(unixepoch(created_at), 1700000000) as created_at 
            FROM post
        """)
        return [dict(row) for row in cursor.fetchall()]

def get_global_post_likes() -> dict[int, int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT post_id, COUNT(*) FROM user_like GROUP BY post_id")
        return {row[0]: row[1] for row in cursor.fetchall()}

def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(SCHEMA)

        # Add table for followers
        conn.execute("""
                CREATE TABLE IF NOT EXISTS user_follow (
                    follower_id INTEGER NOT NULL,
                    followed_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (follower_id, followed_id),
                    FOREIGN KEY (follower_id) REFERENCES user(id),
                    FOREIGN KEY (followed_id) REFERENCES user(id)
                )
            """)

        # Add table for likes
        conn.execute("""
                CREATE TABLE IF NOT EXISTS user_like (
                    user_id INTEGER NOT NULL,
                    post_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (user_id, post_id),
                    FOREIGN KEY (user_id) REFERENCES user(id),
                    FOREIGN KEY (post_id) REFERENCES post(id)
                )
            """)
        conn.commit()


if __name__ == "__main__":
    init_db()
    print(f"Initialized database at {DB_PATH}")

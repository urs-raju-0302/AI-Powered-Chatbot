import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "chatbot.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            intent TEXT NOT NULL,
            confidence REAL NOT NULL,
            bot_response TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_chat(user_message, intent, confidence, bot_response):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO conversations
        (user_message, intent, confidence, bot_response, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user_message,
            intent,
            confidence,
            bot_response,
            datetime.now().isoformat(timespec="seconds"),
        ),
    )
    conn.commit()
    conn.close()


def get_recent_chats(limit=50):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT id, user_message, intent, confidence, bot_response, created_at
        FROM conversations
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "user_message": row[1],
            "intent": row[2],
            "confidence": row[3],
            "bot_response": row[4],
            "created_at": row[5],
        }
        for row in rows
    ]

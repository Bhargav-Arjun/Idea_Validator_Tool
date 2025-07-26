# app/utils/rate_limiter.py
import sqlite3
from datetime import datetime
from app.utils.config import CONFIG

def init_db():
    conn = sqlite3.connect("usage.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usage_limit (
            user_id TEXT,
            date TEXT,
            count INTEGER DEFAULT 0,
            PRIMARY KEY (user_id, date)
        )
    """)
    conn.commit()
    conn.close()

def allow_request(user_id: str) -> bool:
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect("usage.db")
    cursor = conn.cursor()

    cursor.execute("SELECT count FROM usage_limit WHERE user_id = ? AND date = ?", (user_id, today))
    row = cursor.fetchone()

    if row and row[0] >= CONFIG["ALLOWED_PROMPTS_PER_DAY"]:
        return False

    if row:
        cursor.execute("UPDATE usage_limit SET count = count + 1 WHERE user_id = ? AND date = ?", (user_id, today))
    else:
        cursor.execute("INSERT INTO usage_limit (user_id, date, count) VALUES (?, ?, ?)", (user_id, today, 1))

    conn.commit()
    conn.close()
    return True

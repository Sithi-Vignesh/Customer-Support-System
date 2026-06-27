import sqlite3
from datetime import datetime

DB_PATH = "memory.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT NOT NULL,
            query TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_conversation(customer_id: str, query: str, response: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO conversations (customer_id, query, response, timestamp)
        VALUES (?, ?, ?, ?)
    """, (customer_id, query, response, datetime.now().isoformat()))
    conn.commit()
    conn.close()


def get_conversation_history(customer_id: str) -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT query, response, timestamp 
        FROM conversations 
        WHERE customer_id = ? 
        ORDER BY timestamp ASC
    """, (customer_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"query": r[0], "response": r[1], "timestamp": r[2]} for r in rows]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        candidate_name TEXT,
        payload TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()

def save_session(session: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("REPLACE INTO sessions(session_id, candidate_name, payload) VALUES (?,?,?);",
              (session["session_id"], session["candidate_name"], json.dumps(session)))
    conn.commit()
    conn.close()


# db.py
# -----------------------------
# Simple SQLite-based persistence for PoC session storage.
# In production, replace with PostgreSQL or cloud DB.

import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "data", "poc_store.db")

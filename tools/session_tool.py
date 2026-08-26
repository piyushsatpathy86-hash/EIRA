# ============================================================
# EIRA — Session Manager (SQLite) — Per User
# ============================================================

import sys
sys.path.append("C:/EIRA")

import sqlite3
import json
from datetime import datetime
from config.settings import DATA_DIR

DB_PATH = f"{DATA_DIR}/sessions.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            user_id TEXT DEFAULT 'anonymous',
            title TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            agent TEXT,
            model TEXT,
            timestamp TEXT
        )
    ''')
    # user_id column add karo agar nahi hai
    try:
        c.execute('ALTER TABLE sessions ADD COLUMN user_id TEXT DEFAULT "anonymous"')
    except:
        pass
    conn.commit()
    conn.close()

def create_session(session_id: str, title: str = "New Chat", user_id: str = "anonymous"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute('''
        INSERT OR IGNORE INTO sessions (id, user_id, title, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (session_id, user_id, title, now, now))
    conn.commit()
    conn.close()

def save_message(session_id: str, role: str, content: str,
                 agent: str = "", model: str = ""):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute('''
        INSERT INTO messages (session_id, role, content, agent, model, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (session_id, role, content, agent, model, now))
    c.execute('UPDATE sessions SET updated_at = ? WHERE id = ?', (now, session_id))
    conn.commit()
    conn.close()

def get_sessions(user_id: str = "anonymous"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT id, title, updated_at FROM sessions
        WHERE user_id = ?
        ORDER BY updated_at DESC LIMIT 20
    ''', (user_id,))
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "title": r[1], "updated_at": r[2]} for r in rows]

def get_messages(session_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT role, content, agent, model, timestamp
        FROM messages WHERE session_id = ?
        ORDER BY id ASC
    ''', (session_id,))
    rows = c.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1], "agent": r[2],
             "model": r[3], "timestamp": r[4]} for r in rows]

def update_session_title(session_id: str, title: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE sessions SET title = ? WHERE id = ?', (title, session_id))
    conn.commit()
    conn.close()

def delete_session(session_id: str, user_id: str = "anonymous"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM messages WHERE session_id = ?', (session_id,))
    c.execute('DELETE FROM sessions WHERE id = ? AND user_id = ?', (session_id, user_id))
    conn.commit()
    conn.close()

init_db()
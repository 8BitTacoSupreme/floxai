"""
FloxAI Database - Flox-aware data management
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from app.core.config import get_settings

def init_db():
    """Initialize the database with Flox environment info"""
    settings = get_settings()
    db_path = Path(settings.db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(settings.db_path)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY,
            session_id TEXT,
            role TEXT,
            content TEXT,
            timestamp TEXT,
            model_used TEXT,
            response_time REAL,
            flox_env TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY,
            session_id TEXT,
            message_id INTEGER,
            query_text TEXT,
            response_text TEXT,
            worked BOOLEAN DEFAULT FALSE,
            timestamp TEXT,
            flox_env TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flox_environment_info (
            id INTEGER PRIMARY KEY,
            env_name TEXT,
            project_dir TEXT,
            floxai_version TEXT,
            system_info TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    
    # Store current Flox environment info
    flox_info = settings.get_flox_info()
    cursor.execute('''
        INSERT OR REPLACE INTO flox_environment_info 
        (id, env_name, project_dir, floxai_version, system_info, created_at, updated_at)
        VALUES (1, ?, ?, ?, ?, ?, ?)
    ''', (
        flox_info["environment_name"],
        flox_info["project_directory"], 
        flox_info["floxai_version"],
        json.dumps(flox_info["system_info"]),
        datetime.now().isoformat(),
        datetime.now().isoformat()
    ))
    
    conn.commit()
    conn.close()

def save_chat_message(session_id: str, role: str, content: str, 
                     model_used: Optional[str] = None, response_time: Optional[float] = None) -> int:
    """Save a chat message with Flox environment context"""
    settings = get_settings()
    conn = sqlite3.connect(settings.db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO chat_messages (session_id, role, content, timestamp, model_used, response_time, flox_env)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (session_id, role, content, datetime.now().isoformat(), model_used, response_time, settings.flox_env_name))
    
    message_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return message_id

def get_chat_history(session_id: str, limit: int = 50) -> List[Dict]:
    """Get chat history"""
    settings = get_settings()
    conn = sqlite3.connect(settings.db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, role, content, timestamp, model_used, response_time, flox_env
        FROM chat_messages 
        WHERE session_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (session_id, limit))
    
    messages = []
    for row in cursor.fetchall():
        messages.append({
            "id": row[0],
            "role": row[1], 
            "content": row[2],
            "timestamp": row[3],
            "model_used": row[4],
            "response_time": row[5],
            "flox_env": row[6]
        })
    
    conn.close()
    return list(reversed(messages))

def save_feedback(session_id: str, message_id: int, query_text: str, 
                 response_text: str, worked: bool = False) -> int:
    """Save feedback with Flox environment context"""
    settings = get_settings()
    conn = sqlite3.connect(settings.db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO feedback (session_id, message_id, query_text, response_text, worked, timestamp, flox_env)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (session_id, message_id, query_text, response_text, worked, datetime.now().isoformat(), settings.flox_env_name))
    
    feedback_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return feedback_id

def get_flox_stats() -> Dict:
    """Get Flox-specific statistics"""
    settings = get_settings()
    conn = sqlite3.connect(settings.db_path)
    cursor = conn.cursor()
    
    try:
        # Get environment info
        cursor.execute('SELECT * FROM flox_environment_info WHERE id = 1')
        env_row = cursor.fetchone()
        
        # Get usage stats
        cursor.execute('SELECT COUNT(*) FROM chat_messages')
        total_messages = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM feedback WHERE worked = 1')
        successful_interactions = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT session_id) FROM chat_messages')
        unique_sessions = cursor.fetchone()[0]
        
        flox_info = {
            "environment": {
                "name": env_row[1] if env_row else "unknown",
                "project_dir": env_row[2] if env_row else "unknown",
                "version": env_row[3] if env_row else "unknown",
                "system_info": json.loads(env_row[4]) if env_row else {}
            },
            "usage_stats": {
                "total_messages": total_messages,
                "successful_interactions": successful_interactions,
                "unique_sessions": unique_sessions,
                "success_rate": round(successful_interactions / max(total_messages, 1) * 100, 1)
            }
        }
        
        conn.close()
        return flox_info
        
    except Exception as e:
        conn.close()
        return {"error": str(e)}

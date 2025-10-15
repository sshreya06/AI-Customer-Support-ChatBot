import sqlite3
import json
from datetime import datetime
from config import Config

class Database:
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                session_id TEXT PRIMARY KEY,
                messages TEXT,
                created_at TEXT,
                escalated INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_conversation(self, session_id, messages, escalated=False):
        """Save or update a conversation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO conversations (session_id, messages, created_at, escalated)
            VALUES (?, ?, ?, ?)
        ''', (session_id, json.dumps(messages), datetime.now().isoformat(), int(escalated)))
        
        conn.commit()
        conn.close()
    
    def get_conversation(self, session_id):
        """Retrieve a conversation by session ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT messages, escalated FROM conversations WHERE session_id = ?', (session_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'messages': json.loads(result[0]),
                'escalated': bool(result[1])
            }
        return None
    
    def get_all_conversations(self):
        """Get all conversation sessions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT session_id, created_at, escalated FROM conversations ORDER BY created_at DESC')
        results = cursor.fetchall()
        conn.close()
        
        conversations = []
        for result in results:
            conversations.append({
                'session_id': result[0],
                'created_at': result[1],
                'escalated': bool(result[2])
            })
        
        return conversations
    
    def delete_conversation(self, session_id):
        """Delete a conversation by session ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if conversation exists
        cursor.execute('SELECT session_id FROM conversations WHERE session_id = ?', (session_id,))
        exists = cursor.fetchone()
        
        if exists:
            cursor.execute('DELETE FROM conversations WHERE session_id = ?', (session_id,))
            conn.commit()
            conn.close()
            return True
        
        conn.close()
        return False
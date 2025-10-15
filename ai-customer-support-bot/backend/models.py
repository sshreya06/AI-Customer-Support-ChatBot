from datetime import datetime

class Conversation:
    def __init__(self, session_id):
        self.session_id = session_id
        self.messages = []
        self.created_at = datetime.now()
        self.escalated = False
    
    def add_message(self, role, content):
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        }
        self.messages.append(message)
        return message
    
    def get_history(self):
        return self.messages
    
    def escalate(self):
        self.escalated = True
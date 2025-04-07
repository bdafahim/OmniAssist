from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class Message(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime = datetime.now()

class Conversation(BaseModel):
    session_id: str
    messages: List[Message] = []
    context: Dict = {}
    business_type: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    def add_message(self, role: str, content: str):
        message = Message(role=role, content=content)
        self.messages.append(message)
        self.updated_at = datetime.now()

    def get_context(self) -> Dict:
        return self.context

    def update_context(self, key: str, value: any):
        self.context[key] = value
        self.updated_at = datetime.now()

class BusinessConfig(BaseModel):
    type: str
    name: str
    settings: Dict
    knowledge_base: Optional[Dict] = None 
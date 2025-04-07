from typing import Dict, Optional
from app.models.conversation import Conversation, Message
import uuid
from datetime import datetime

class ConversationManager:
    def __init__(self):
        self.conversations: Dict[str, Conversation] = {}

    
    def create_conversation(self, business_type: str, session_id: Optional[str] = None) -> Conversation:
        if session_id is None:
            session_id = str(uuid.uuid4())
        conversation = Conversation(
            session_id=session_id,
            business_type=business_type
        )
        self.conversations[session_id] = conversation
        return conversation

    def get_conversation(self, session_id: str) -> Optional[Conversation]:
        """
        Retrieve an existing conversation
        """
        return self.conversations.get(session_id)

    def add_message(self, session_id: str, role: str, content: str):
        """
        Add a message to an existing conversation
        """
        conversation = self.get_conversation(session_id)
        if conversation:
            conversation.add_message(role, content)
        else:
            raise ValueError(f"Conversation {session_id} not found")

    def update_context(self, session_id: str, key: str, value: any):
        """
        Update the context of a conversation
        """
        conversation = self.get_conversation(session_id)
        if conversation:
            conversation.update_context(key, value)
        else:
            raise ValueError(f"Conversation {session_id} not found")

    def get_conversation_history(self, session_id: str) -> list:
        """
        Get the message history of a conversation
        """
        conversation = self.get_conversation(session_id)
        if conversation:
            return [{"role": msg.role, "content": msg.content, "timestamp": msg.timestamp} 
                   for msg in conversation.messages]
        return []

    def end_conversation(self, session_id: str):
        """
        End and clean up a conversation
        """
        if session_id in self.conversations:
            del self.conversations[session_id] 
from typing import Dict, List, Optional
import json
import os
from app.core.config import settings
from app.services.knowledge_service import KnowledgeService

class LanguageService:
    def __init__(self):
        self.business_type = settings.BUSINESS_TYPE
        self.responses = self._load_responses()
        self.knowledge_service = KnowledgeService()

    def _load_responses(self) -> Dict:
        """
        Load predefined responses based on business type
        """
        # Default responses for different business types
        default_responses = {
            "restaurant": {
                "greeting": "Welcome to our restaurant! How can I help you today?",
                "menu_inquiry": "Our menu includes appetizers, main courses, and desserts. What would you like to know more about?",
                "order_confirmation": "I've noted your order. Is there anything else you'd like to add?",
                "goodbye": "Thank you for your order! We look forward to serving you.",
                "fallback": "I'm not sure I understood. Could you please repeat that?"
            },
            "real_estate": {
                "greeting": "Welcome to our real estate agency! How can I assist you today?",
                "property_inquiry": "We have several properties available. What type of property are you looking for?",
                "viewing_scheduling": "I can help you schedule a viewing. What day and time works for you?",
                "goodbye": "Thank you for your interest! We'll be in touch soon.",
                "fallback": "I'm not sure I understood. Could you please repeat that?"
            }
        }
        
        return default_responses.get(self.business_type, default_responses["restaurant"])

    async def generate_response(self, user_input: str, conversation_history: List[Dict]) -> str:
        """
        Generate a response based on user input and conversation history
        """
        # Query the knowledge base
        knowledge_result = await self.knowledge_service.query_knowledge_base(user_input)
        
        # Generate a response based on the knowledge base result
        if knowledge_result["type"] == "menu":
            menu_data = knowledge_result["data"]
            if "appetizers" in user_input.lower():
                items = menu_data.get("appetizers", [])
                return f"Our appetizers include: {', '.join([item['name'] for item in items])}. What would you like to know more about?"
            elif "main" in user_input.lower() or "entree" in user_input.lower():
                items = menu_data.get("main_courses", [])
                return f"Our main courses include: {', '.join([item['name'] for item in items])}. What would you like to know more about?"
            elif "dessert" in user_input.lower():
                items = menu_data.get("desserts", [])
                return f"Our desserts include: {', '.join([item['name'] for item in items])}. What would you like to know more about?"
            else:
                return "Our menu includes appetizers, main courses, and desserts. What would you like to know more about?"
        elif knowledge_result["type"] == "hours":
            return f"We are open {knowledge_result['data']}."
        elif knowledge_result["type"] == "location":
            return f"We are located at {knowledge_result['data']}."
        elif knowledge_result["type"] == "contact":
            return f"You can reach us at {knowledge_result['data']}."
        elif knowledge_result["type"] == "properties":
            properties = knowledge_result["data"]
            if len(properties) > 0:
                return f"We have {len(properties)} properties available. What type of property are you looking for?"
            else:
                return "We don't have any properties available at the moment."
        elif knowledge_result["type"] == "agents":
            agents = knowledge_result["data"]
            if len(agents) > 0:
                return f"We have {len(agents)} agents available to help you. Would you like to speak with one of them?"
            else:
                return "We don't have any agents available at the moment."
        
        # If no specific knowledge base response, use keyword-based response generation
        user_input_lower = user_input.lower()
        
        # Check for common keywords
        if any(word in user_input_lower for word in ["menu", "food", "eat", "order"]):
            return self.responses["menu_inquiry"]
        elif any(word in user_input_lower for word in ["property", "house", "apartment", "real estate"]):
            return self.responses["property_inquiry"]
        elif any(word in user_input_lower for word in ["bye", "goodbye", "thank you", "thanks"]):
            return self.responses["goodbye"]
        elif any(word in user_input_lower for word in ["order", "place", "want", "would like"]):
            return self.responses["order_confirmation"]
        elif any(word in user_input_lower for word in ["schedule", "viewing", "appointment", "meet"]):
            return self.responses["viewing_scheduling"]
        else:
            return self.responses["fallback"]

    async def analyze_sentiment(self, text: str) -> Dict:
        """
        Simple sentiment analysis
        """
        positive_words = ["good", "great", "excellent", "amazing", "love", "like", "happy", "pleased"]
        negative_words = ["bad", "terrible", "awful", "hate", "dislike", "unhappy", "angry", "disappointed"]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = "positive"
        elif negative_count > positive_count:
            sentiment = "negative"
        else:
            sentiment = "neutral"
            
        return {
            "sentiment": sentiment,
            "positive_score": positive_count,
            "negative_score": negative_count
        } 
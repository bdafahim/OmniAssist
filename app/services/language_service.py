from typing import Dict, List, Optional
import json
import os
from app.core.config import settings
from app.services.knowledge_service import KnowledgeService
from transformers import pipeline

class LanguageService:
    def __init__(self):
        self.business_type = settings.BUSINESS_TYPE
        self.responses = self._load_responses()
        self.knowledge_service = KnowledgeService()
        # Initialize a text-generation pipeline using a model like GPT-2
        self.generator = pipeline("text-generation", model="gpt2")

    def _load_responses(self) -> Dict:
        """
        Load predefined responses based on business type
        """
        # Enhanced restaurant responses
        default_responses = {
            "restaurant": {
                "greeting": "Welcome to our restaurant! How can I help you today?",
                "menu_inquiry": "Our menu includes appetizers, main courses, and desserts. What would you like to know more about?",
                "order_confirmation": "I've noted your order. Is there anything else you'd like to add?",
                "goodbye": "Thank you for your order! We look forward to serving you.",
                "fallback": "I'm not sure I understood. Could you please repeat that?",
                "menu_categories": {
                    "appetizers": "Our appetizers include: {items}. Would you like to know more about any specific item?",
                    "main_courses": "Our main courses include: {items}. What would you like to know more about?",
                    "desserts": "Our desserts include: {items}. Would you like to try any of these?",
                    "beverages": "We offer: {items}. What would you like to drink?"
                },
                "order_phrases": {
                    "start_order": "I'd like to place an order",
                    "add_item": "I want to add",
                    "remove_item": "I want to remove",
                    "modify_item": "Can I change",
                    "special_requests": "I have a special request"
                },
                "menu_questions": {
                    "ingredients": "What are the ingredients in",
                    "allergens": "Does this contain",
                    "spiciness": "How spicy is",
                    "portion_size": "How big is the portion of",
                    "price": "How much does",
                    "recommendations": "What do you recommend"
                },
                "order_status": {
                    "check_status": "What's the status of my order",
                    "estimated_time": "How long will it take",
                    "delivery_time": "When will it be delivered",
                    "pickup_time": "When can I pick it up"
                },
                "special_requests": {
                    "dietary_restrictions": "I have dietary restrictions",
                    "allergies": "I have allergies",
                    "preferences": "I prefer",
                    "customization": "Can you customize"
                }
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

    async def generate_response(self, user_input: str, conversation_history: list) -> str:
        """
        Generate a response using a transformer-based model with enhanced restaurant patterns.
        """
        # Check for specific restaurant patterns
        user_input_lower = user_input.lower()
        
        # Menu category inquiries
        if any(word in user_input_lower for word in ["appetizer", "starter", "snack"]):
            return self._handle_menu_category("appetizers")
        elif any(word in user_input_lower for word in ["main", "entree", "dish", "meal"]):
            return self._handle_menu_category("main_courses")
        elif any(word in user_input_lower for word in ["dessert", "sweet", "cake"]):
            return self._handle_menu_category("desserts")
        elif any(word in user_input_lower for word in ["drink", "beverage", "wine", "beer"]):
            return self._handle_menu_category("beverages")
            
        # Order-related patterns
        if any(phrase in user_input_lower for phrase in ["place an order", "want to order", "would like to order"]):
            return "I'd be happy to take your order. What would you like to start with?"
        elif any(phrase in user_input_lower for phrase in ["add to my order", "add this", "also want"]):
            return "I'll add that to your order. Would you like anything else?"
        elif any(phrase in user_input_lower for phrase in ["remove from my order", "take this off", "don't want"]):
            return "I'll remove that from your order. Is there anything else you'd like to change?"
            
        # Menu questions
        if any(phrase in user_input_lower for phrase in ["what's in", "ingredients in", "made with"]):
            return "Let me check the ingredients for you. Which item would you like to know about?"
        elif any(phrase in user_input_lower for phrase in ["contains", "allergens", "allergic"]):
            return "I can check for allergens. Which item are you concerned about?"
        elif any(phrase in user_input_lower for phrase in ["how spicy", "spice level", "heat level"]):
            return "I can tell you about the spice level. Which dish would you like to know about?"
            
        # Special requests
        if any(phrase in user_input_lower for phrase in ["vegetarian", "vegan", "gluten-free"]):
            return "We have several options available. Would you like to see our {dietary_restriction} menu?"
        elif any(phrase in user_input_lower for phrase in ["allergy", "allergic to", "can't eat"]):
            return "Please let me know about your allergies, and I'll help you find safe options."
            
        # Order status
        if any(phrase in user_input_lower for phrase in ["status of my order", "where is my order", "how long"]):
            return "Let me check the status of your order. Could you please provide your order number?"
            
        # If no specific pattern matches, use the transformer model
        prompt = "Conversation:\n"
        for message in conversation_history:
            prompt += f"{message['role']}: {message['content']}\n"
        prompt += f"user: {user_input}\nassistant:"
        
        result = self.generator(prompt, max_length=500, num_return_sequences=1)
        generated_text = result[0]['generated_text']
        response = generated_text[len(prompt):].split("\n")[0].strip()
        print('Generated from Gpt 2')
        
        return response if response else self.responses["fallback"]

    def _handle_menu_category(self, category: str) -> str:
        """Handle menu category inquiries"""
        menu_data = self.knowledge_service.get_menu_data()
        if menu_data and category in menu_data:
            items = [item['name'] for item in menu_data[category]]
            return self.responses["menu_categories"][category].format(items=", ".join(items))
        return self.responses["fallback"]

    async def analyze_sentiment(self, text: str) -> Dict:
        """
        Enhanced sentiment analysis with restaurant-specific terms
        """
        positive_words = [
            "good", "great", "excellent", "amazing", "love", "like", "happy", "pleased",
            "delicious", "tasty", "wonderful", "perfect", "favorite", "recommend", "enjoy"
        ]
        negative_words = [
            "bad", "terrible", "awful", "hate", "dislike", "unhappy", "angry", "disappointed",
            "overcooked", "undercooked", "cold", "spicy", "bland", "expensive", "slow"
        ]
        
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
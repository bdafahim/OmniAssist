from typing import Dict, List, Optional
import os
import json
from app.core.config import settings

class KnowledgeService:
    def __init__(self):
        self.business_type = settings.BUSINESS_TYPE
        self.knowledge_base = self._load_knowledge_base()
        
    def _load_knowledge_base(self) -> Dict:
        """
        Load knowledge base based on business type
        """
        # Default knowledge bases for different business types
        default_knowledge_bases = {
            "restaurant": {
                "menu": {
                    "appetizers": [
                        {"name": "Bruschetta", "price": 8.99, "description": "Toasted bread with tomatoes, garlic, and basil"},
                        {"name": "Calamari", "price": 12.99, "description": "Fried squid rings with marinara sauce"},
                        {"name": "Wings", "price": 10.99, "description": "Buffalo wings with blue cheese dressing"}
                    ],
                    "main_courses": [
                        {"name": "Pasta Carbonara", "price": 16.99, "description": "Spaghetti with pancetta, egg, and parmesan"},
                        {"name": "Grilled Salmon", "price": 22.99, "description": "Fresh salmon with lemon butter sauce"},
                        {"name": "Beef Tenderloin", "price": 29.99, "description": "8oz tenderloin with mushroom sauce"}
                    ],
                    "desserts": [
                        {"name": "Tiramisu", "price": 7.99, "description": "Classic Italian dessert with coffee and mascarpone"},
                        {"name": "Chocolate Cake", "price": 6.99, "description": "Rich chocolate cake with ganache"},
                        {"name": "Ice Cream", "price": 5.99, "description": "Vanilla, chocolate, or strawberry"}
                    ]
                },
                "hours": "Monday-Sunday: 11am-10pm",
                "location": "123 Main St, Anytown, USA",
                "contact": "555-123-4567"
            },
            "real_estate": {
                "properties": [
                    {
                        "id": "1",
                        "type": "House",
                        "address": "123 Oak St, Anytown, USA",
                        "price": 350000,
                        "bedrooms": 3,
                        "bathrooms": 2,
                        "square_feet": 2000,
                        "description": "Beautiful family home with large backyard"
                    },
                    {
                        "id": "2",
                        "type": "Apartment",
                        "address": "456 Pine Ave, Anytown, USA",
                        "price": 250000,
                        "bedrooms": 2,
                        "bathrooms": 1,
                        "square_feet": 1200,
                        "description": "Modern apartment in downtown area"
                    },
                    {
                        "id": "3",
                        "type": "Condo",
                        "address": "789 Maple Dr, Anytown, USA",
                        "price": 300000,
                        "bedrooms": 2,
                        "bathrooms": 2,
                        "square_feet": 1500,
                        "description": "Luxury condo with city views"
                    }
                ],
                "agents": [
                    {"name": "John Smith", "phone": "555-123-4567", "email": "john@example.com"},
                    {"name": "Jane Doe", "phone": "555-987-6543", "email": "jane@example.com"}
                ],
                "office_hours": "Monday-Friday: 9am-5pm, Saturday: 10am-2pm",
                "location": "789 Real Estate Ave, Anytown, USA",
                "contact": "555-555-5555"
            }
        }
        
        return default_knowledge_bases.get(self.business_type, default_knowledge_bases["restaurant"])
        
    async def query_knowledge_base(self, query: str) -> Dict:
        """
        Query the knowledge base based on the user's question
        """
        query_lower = query.lower()
        
        # Simple keyword-based querying
        if "menu" in query_lower or "food" in query_lower or "eat" in query_lower:
            return {"type": "menu", "data": self.knowledge_base.get("menu", {})}
        elif "hours" in query_lower or "open" in query_lower or "close" in query_lower:
            return {"type": "hours", "data": self.knowledge_base.get("hours", "Hours not available")}
        elif "location" in query_lower or "address" in query_lower or "where" in query_lower:
            return {"type": "location", "data": self.knowledge_base.get("location", "Location not available")}
        elif "contact" in query_lower or "phone" in query_lower or "call" in query_lower:
            return {"type": "contact", "data": self.knowledge_base.get("contact", "Contact not available")}
        elif "property" in query_lower or "house" in query_lower or "apartment" in query_lower:
            return {"type": "properties", "data": self.knowledge_base.get("properties", [])}
        elif "agent" in query_lower or "realtor" in query_lower or "broker" in query_lower:
            return {"type": "agents", "data": self.knowledge_base.get("agents", [])}
        else:
            return {"type": "unknown", "data": "I don't have information about that."}
            
    async def update_knowledge_base(self, data: Dict):
        """
        Update the knowledge base with new information
        
        Note: In a real implementation, this would update a database or vector store
        """
        # In a real implementation, this would update a database or vector store
        # For now, we'll just update our in-memory knowledge base
        for key, value in data.items():
            self.knowledge_base[key] = value 
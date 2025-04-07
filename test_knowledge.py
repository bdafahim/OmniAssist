import asyncio
import os
import sys

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.knowledge_service import KnowledgeService
from app.core.config import settings

async def test_knowledge_service():
    print(f"Testing Knowledge Service for business type: {settings.BUSINESS_TYPE}")
    
    knowledge_service = KnowledgeService()
    
    # Test queries
    queries = [
        "What's on the menu?",
        "What are your hours?",
        "Where are you located?",
        "How can I contact you?",
        "What properties do you have?",
        "Who are your agents?"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        result = await knowledge_service.query_knowledge_base(query)
        print(f"Result type: {result['type']}")
        print(f"Result data: {result['data']}")

if __name__ == "__main__":
    asyncio.run(test_knowledge_service()) 
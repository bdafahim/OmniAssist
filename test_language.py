import asyncio
import os
import sys

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.language_service import LanguageService

async def test_language_service():
    print("Testing Language Service")
    
    language_service = LanguageService()
    
    # Test inputs
    inputs = [
        "What's on the menu?",
        "I'd like to order some food",
        "What are your appetizers?",
        "What are your main courses?",
        "What are your desserts?",
        "What are your hours?",
        "Where are you located?",
        "How can I contact you?",
        "What properties do you have?",
        "Who are your agents?",
        "I'd like to schedule a viewing",
        "Thank you, goodbye"
    ]
    
    for user_input in inputs:
        print(f"\nUser input: {user_input}")
        response = await language_service.generate_response(user_input, [])
        print(f"Response: {response}")
        
        sentiment = await language_service.analyze_sentiment(user_input)
        print(f"Sentiment: {sentiment['sentiment']} (positive: {sentiment['positive_score']}, negative: {sentiment['negative_score']})")

if __name__ == "__main__":
    asyncio.run(test_language_service()) 
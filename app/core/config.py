import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Customer Service & Ordering Agent"
    
    # Twilio Settings
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_PHONE_NUMBER: str = os.getenv("TWILIO_PHONE_NUMBER", "")
    
    # Pinecone Settings
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT", "")
    
    # AI Model Settings
    WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "base")  # Options: tiny, base, small, medium, large
    LANGUAGE_MODEL: str = os.getenv("LANGUAGE_MODEL", "llama2-7b")  # Default language model
    
    # Business Settings
    BUSINESS_TYPE: str = os.getenv("BUSINESS_TYPE", "restaurant")  # Default business type

settings = Settings() 
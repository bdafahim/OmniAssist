# AI Customer Service & Ordering Agent

An AI-powered customer service and ordering agent that can interact with customers via phone calls in a human-like manner.

## Features

- Multi-business adaptability (restaurant, real estate, etc.)
- Human-like conversational ability
- Real-time call handling with Twilio
- Dynamic knowledge base integration
- Context retention & memory
- Ordering & inquiry handling
- Sentiment analysis
- Speech-to-text conversion with Whisper
- Text-to-speech capability (placeholder for Piper integration)

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with the following variables:
```
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=your_twilio_phone
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENVIRONMENT=your_pinecone_env
WHISPER_MODEL=base
LANGUAGE_MODEL=llama2-7b
BUSINESS_TYPE=restaurant
```

4. Run the application:
```bash
python test_app.py
```

## Project Structure

```
.
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── api/                 # API routes
│   │   ├── voice.py         # Voice call handling
│   │   └── knowledge.py     # Knowledge base API
│   ├── core/               # Core functionality
│   │   └── config.py       # Configuration settings
│   ├── models/             # Data models
│   │   └── conversation.py # Conversation models
│   ├── services/           # Business logic
│   │   ├── conversation_manager.py # Conversation management
│   │   ├── knowledge_service.py    # Knowledge base service
│   │   ├── language_service.py     # Language processing
│   │   ├── speech_service.py       # Speech-to-text
│   │   └── tts_service.py          # Text-to-speech
│   └── utils/              # Utility functions
├── tests/                  # Test files
├── .env                    # Environment variables
├── requirements.txt        # Project dependencies
├── setup.sh                # Setup script
├── test_app.py             # Application test script
├── test_knowledge.py       # Knowledge service test
├── test_language.py        # Language service test
└── README.md              # Project documentation
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

You can test individual components using the provided test scripts:

```bash
# Test the knowledge base service
python test_knowledge.py

# Test the language service
python test_language.py

# Test the full application
python test_app.py
```

## Business Types

The system supports different business types, which can be configured in the `.env` file:

- `restaurant`: For restaurant ordering and inquiries
- `real_estate`: For real estate property inquiries and viewing scheduling

## Next Steps

- Integrate with Llama for more advanced language processing
- Integrate with Pinecone for vector-based knowledge retrieval
- Integrate with Piper for text-to-speech
- Add database integration for persistent storage
- Implement authentication and authorization
- Add more business types and knowledge bases 
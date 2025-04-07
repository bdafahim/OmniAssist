# AI Customer Service & Ordering Agent

An AI-powered customer service and ordering agent that can interact with customers via phone calls and SMS in a human-like manner.

## Features

- Multi-business adaptability (restaurant, real estate, etc.)
- SMS-based customer interaction
- Human-like conversational ability
- Dynamic knowledge base integration with web interface
- Real-time call handling with Twilio
- Context retention & memory
- Ordering & inquiry handling
- Sentiment analysis
- Speech-to-text conversion with Whisper
- Text-to-speech capability

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
│   │   ├── sms.py          # SMS handling
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
│   ├── templates/          # HTML templates
│   │   ├── index.html     # Main chat interface
│   │   └── knowledge_update.html   # Knowledge update form
│   └── static/            # Static files
├── tests/                  # Test files
│   ├── test_knowledge.py  # Knowledge service tests
│   ├── test_language.py   # Language service tests
│   ├── test_config.py     # Configuration tests
│   ├── test_websocket.py  # WebSocket tests
│   └── test.wav           # Test audio file
├── .env                    # Environment variables
├── requirements.txt        # Project dependencies
├── setup.sh                # Setup script
├── test_app.py             # Application test script
└── README.md              # Project documentation
```

## Features in Detail

### SMS Service
- Real-time SMS conversation handling
- Context-aware responses
- Conversation history tracking
- Phone number normalization
- Error handling and logging
- Test mode with consistent phone number

### Knowledge Base Management
- Web interface for updating business information
- Support for multiple business types (restaurant, real estate)
- Dynamic form generation based on business type
- Real-time validation and error handling
- Success/failure notifications
- Persistent storage of business data

#### Restaurant Business Type
- Menu management (appetizers, main courses, etc.)
- Business hours updates
- Price and description management
- Special requests handling

#### Real Estate Business Type
- Property listing management
- Property details (price, bedrooms, bathrooms, etc.)
- Property descriptions
- Location information

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key API Endpoints

#### SMS Endpoints
- `POST /api/v1/sms/` - Handle incoming SMS messages
- `GET /api/v1/sms/conversation` - Get conversation history
- `GET /api/v1/sms/status` - Check SMS service status

#### Knowledge Base Endpoints
- `POST /api/v1/knowledge/update` - Update business information
- `GET /api/v1/knowledge/query` - Query the knowledge base
- `GET /api/v1/knowledge/menu` - Get menu information (restaurant)
- `GET /api/v1/knowledge/properties` - Get property listings (real estate)

## Testing

You can test individual components using the provided test scripts:

```bash

# Test the full application
python test_app.py

# Test the knowledge base service
python tests/test_knowledge.py

# Test the language service
python tests/test_language.py

# Test the configuration
python tests/test_config.py

# Test WebSocket functionality
python tests/test_websocket.py
```

## Web Interface

The application provides a web interface at http://localhost:8000/ with:

1. Chat Interface
   - Real-time message display
   - Message history
   - Loading indicators
   - Error handling

2. Knowledge Update Interface
   - Business type selection
   - Dynamic form generation
   - Real-time validation
   - Success/error notifications
   - Modal dialog interface

## Business Types

The system supports different business types, which can be configured in the `.env` file:

- `restaurant`: For restaurant ordering and inquiries
  - Menu management
  - Order handling
  - Special requests
  - Business hours

- `real_estate`: For real estate property inquiries
  - Property listings
  - Viewing scheduling
  - Property details
  - Location information

Note: Currently, the system is configured for the restaurant business type by default, but it can be easily adapted for other business types by modifying the `BUSINESS_TYPE` variable in the `.env` file. The knowledge base and conversation handling are designed to be extensible for different business domains.



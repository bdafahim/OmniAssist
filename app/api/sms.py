from fastapi import APIRouter, Request, HTTPException, Response, Form
from twilio.twiml.messaging_response import MessagingResponse
from app.services.conversation_manager import ConversationManager
from app.services.language_service import LanguageService
from app.core.config import settings
import logging
from typing import Optional, Dict, Any, List
import re

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SMSService")

router = APIRouter(prefix="/sms", tags=["sms"])
conversation_manager = ConversationManager()
language_service = LanguageService()

def normalize_phone_number(phone: str) -> str:
    """
    Normalize phone number to a consistent format
    """
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Add + if not present and ensure 10 digits
    if len(digits) == 10:
        return f"+1{digits}"
    elif digits.startswith('1') and len(digits) == 11:
        return f"+{digits}"
    else:
        return f"+{digits}"

def validate_twilio_request(request: Request) -> bool:
    """
    Validate that the request is coming from Twilio
    """
    try:
        form_data = request.form()
        return bool(form_data.get("From") and form_data.get("Body"))
    except Exception as e:
        logger.error(f"Error validating request: {str(e)}")
        return False

@router.post("/")
async def handle_sms(
    request: Request,
    Body: Optional[str] = Form(None),
    From: Optional[str] = Form(None)
):
    try:
        # Get form data
        form_data: Dict[str, Any] = {}
        try:
            form_data = await request.form()
        except Exception as e:
            logger.warning(f"Could not parse form data: {str(e)}")
            if Body and From:
                form_data = {"Body": Body, "From": From}
        
        message_body = (form_data.get("Body") or "").strip()
        from_number = normalize_phone_number(form_data.get("From") or "")
        
        logger.info(f"Received request with data: {form_data}")
        logger.info(f"Normalized phone number: {from_number}")
        
        if not message_body or not from_number:
            logger.warning(f"Missing required fields. Body: {message_body}, From: {from_number}")
            raise HTTPException(status_code=400, detail="Missing required fields: Body and From")
        
        logger.info(f"Processing SMS from {from_number}: {message_body}")
        
        session_id = from_number
        
        # Create a new conversation if one doesn't exist for this sender
        if not conversation_manager.get_conversation(session_id):
            logger.info(f"Creating new conversation for {from_number}")
            conversation = conversation_manager.create_conversation(settings.BUSINESS_TYPE, session_id)
        else:
            conversation = conversation_manager.get_conversation(session_id)
            logger.info(f"Retrieved existing conversation for {from_number}")
        
        # Log the incoming SMS message
        conversation_manager.add_message(session_id, "user", message_body)
        conversation_history = conversation_manager.get_conversation_history(session_id)
        logger.info(f"Current conversation history: {conversation_history}")
        
        # Generate an AI response using the language service
        ai_response = await language_service.generate_response(message_body, conversation_history)
        
        # Analyze sentiment and update the conversation context
        sentiment = await language_service.analyze_sentiment(message_body)
        conversation_manager.update_context(session_id, "sentiment", sentiment)
        
        # Log the AI-generated response
        conversation_manager.add_message(session_id, "assistant", ai_response)
        
        logger.info(f"Sending response to {from_number}: {ai_response}")
        
        # Create a Twilio MessagingResponse to reply to the SMS
        twilio_response = MessagingResponse()
        twilio_response.message(ai_response)
        
        return Response(content=str(twilio_response), media_type="application/xml")
        
    except HTTPException as he:
        logger.error(f"HTTP error handling SMS: {str(he)}")
        raise he
    except Exception as e:
        logger.error(f"Error handling SMS: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/conversation")
async def get_conversation(From: str = "+1234567890"):
    """
    Get the conversation history for a specific phone number
    """
    try:
        # Normalize the phone number
        session_id = normalize_phone_number(From)
        logger.info(f"Getting conversation for phone number: {session_id}")
        
        conversation = conversation_manager.get_conversation(session_id)
        
        if not conversation:
            logger.info(f"No conversation found for {session_id}")
            return {"messages": []}
            
        messages = conversation_manager.get_conversation_history(session_id)
        logger.info(f"Retrieved {len(messages)} messages for {session_id}")
        return {"messages": messages}
        
    except Exception as e:
        logger.error(f"Error getting conversation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error getting conversation: {str(e)}")
    
@router.get("/status")
async def sms_status():
    """Check if the SMS endpoint is active"""
    return {"status": "SMS endpoint active", "business_type": settings.BUSINESS_TYPE}
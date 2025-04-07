from fastapi import APIRouter, Request, HTTPException, Response
from twilio.twiml.messaging_response import MessagingResponse
from app.services.conversation_manager import ConversationManager
from app.services.language_service import LanguageService
from app.core.config import settings

router = APIRouter(prefix="/sms", tags=["sms"])
conversation_manager = ConversationManager()
language_service = LanguageService()

@router.post("/")
async def handle_sms(request: Request):
    try:
        form_data = await request.form()
        message_body = form_data.get("Body", "")
        from_number = form_data.get("From", "")
        
        session_id = from_number
        
        # Create a new conversation if one doesn't exist for this sender
        if not conversation_manager.get_conversation(session_id):
            conversation = conversation_manager.create_conversation(settings.BUSINESS_TYPE, session_id)
        else:
            conversation = conversation_manager.get_conversation(session_id)
        
        # Log the incoming SMS message
        conversation_manager.add_message(session_id, "user", message_body)
        conversation_history = conversation_manager.get_conversation_history(session_id)
        
        # Generate an AI response using the language service
        ai_response = await language_service.generate_response(message_body, conversation_history)
        
        # Analyze sentiment and update the conversation context
        sentiment = await language_service.analyze_sentiment(message_body)
        conversation_manager.update_context(session_id, "sentiment", sentiment)
        
        # Log the AI-generated response
        conversation_manager.add_message(session_id, "assistant", ai_response)
        
        # Create a Twilio MessagingResponse to reply to the SMS
        twilio_response = MessagingResponse()
        twilio_response.message(ai_response)
        
        return Response(content=str(twilio_response), media_type="application/xml")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/status")
async def sms_status():
    return {"status": "SMS endpoint active"}
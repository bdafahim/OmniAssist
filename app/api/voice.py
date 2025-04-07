from fastapi import APIRouter, Request, HTTPException, WebSocket, WebSocketDisconnect, UploadFile, File
from twilio.twiml.voice_response import VoiceResponse, Gather
from app.services.conversation_manager import ConversationManager
from app.services.speech_service import SpeechService
from app.services.language_service import LanguageService
from app.core.config import settings
from fastapi.responses import JSONResponse
import json

router = APIRouter(prefix="/voice", tags=["voice"])
conversation_manager = ConversationManager()
speech_service = SpeechService()
language_service = LanguageService()

@router.post("/voice")
async def handle_call(request: Request):
    """Handle incoming voice calls"""
    try:
        # Create a new conversation session
        conversation = conversation_manager.create_conversation(settings.BUSINESS_TYPE)
        
        # Create a TwiML response
        response = VoiceResponse()
        
        # Add a greeting
        response.say("Hello! Welcome to our AI customer service. How can I help you today?")
        
        # Gather user input
        gather = Gather(
            input='speech',
            action=f'/api/v1/voice/handle-input?session_id={conversation.session_id}',
            method='POST',
            language='en-US',
            speechTimeout='auto'
        )
        response.append(gather)
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/voice/handle-input")
async def handle_input(request: Request, session_id: str):
    """Handle user speech input"""
    try:
        form_data = await request.form()
        speech_result = form_data.get('SpeechResult', '')
        
        # Add user message to conversation
        conversation_manager.add_message(session_id, "user", speech_result)
        
        # Get conversation history
        conversation_history = conversation_manager.get_conversation_history(session_id)
        
        # Generate response using language service
        ai_response = await language_service.generate_response(speech_result, conversation_history)
        
        # Analyze sentiment
        sentiment = await language_service.analyze_sentiment(speech_result)
        
        # Update conversation context with sentiment
        conversation_manager.update_context(session_id, "sentiment", sentiment)
        
        # Add AI response to conversation
        conversation_manager.add_message(session_id, "assistant", ai_response)
        
        # Create a response
        response = VoiceResponse()
        
        # Say the AI response
        response.say(ai_response)
        
        # Add another gather to continue the conversation
        gather = Gather(
            input='speech',
            action=f'/api/v1/voice/handle-input?session_id={session_id}',
            method='POST',
            language='en-US',
            speechTimeout='auto'
        )
        response.append(gather)
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/voice/conversation/{session_id}")
async def get_conversation(session_id: str):
    """Get conversation history"""
    try:
        history = conversation_manager.get_conversation_history(session_id)
        return {"session_id": session_id, "history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive audio data
            audio_data = await websocket.receive_bytes()
            
            # Process the audio and get transcription
            transcription = await speech_service.transcribe_audio(audio_data)
            
            # Send back the transcription
            await websocket.send_text(json.dumps({
                "transcription": transcription
            }))
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.send_text(json.dumps({
            "error": str(e)
        }))

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        # Read the uploaded file
        audio_data = await file.read()
        
        # Process the audio
        transcription = await speech_service.transcribe_audio(audio_data)
        
        return JSONResponse(content={
            "transcription": transcription
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def voice_status():
    return {
        "status": "active",
        "model": settings.WHISPER_MODEL,
        "service": "whisper"
    } 
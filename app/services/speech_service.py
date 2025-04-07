import whisper
import tempfile
import os
from app.core.config import settings

class SpeechService:
    def __init__(self):
        self.model = None
        self.model_name = settings.WHISPER_MODEL

    def _load_model(self):
        """
        Load the Whisper model lazily
        """
        if self.model is None:
            try:
                self.model = whisper.load_model(self.model_name)
            except Exception as e:
                print(f"Warning: Could not load Whisper model: {str(e)}")
                print("Using placeholder transcription service")

    async def transcribe_audio(self, audio_data: bytes) -> str:
        """
        Transcribe audio data to text using Whisper
        """
        try:
            # Create a temporary file to store the audio data
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(audio_data)
                temp_audio_path = temp_audio.name

            # Load model if not loaded
            self._load_model()

            if self.model is not None:
                # Transcribe the audio file
                result = self.model.transcribe(temp_audio_path)
                text = result["text"]
            else:
                # Placeholder response if model is not available
                text = "I'm sorry, speech recognition is currently unavailable."

            # Clean up the temporary file
            os.unlink(temp_audio_path)

            return text
        except Exception as e:
            return f"Error transcribing audio: {str(e)}"

    async def process_audio_stream(self, audio_stream):
        """
        Process a streaming audio input
        """
        try:
            # Collect the audio data from the stream
            audio_data = b""
            async for chunk in audio_stream:
                audio_data += chunk

            # Transcribe the collected audio
            return await self.transcribe_audio(audio_data)
        except Exception as e:
            return f"Error processing audio stream: {str(e)}" 
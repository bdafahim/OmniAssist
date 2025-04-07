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

    async def process_audio_stream(self, audio_data):
        """
        Process audio data from either a stream or a list of chunks
        """
        try:
            # If audio_data is a list, concatenate the chunks
            if isinstance(audio_data, list):
                audio_bytes = b"".join(audio_data)
            else:
                # If it's an async iterator, collect all chunks
                audio_bytes = b""
                async for chunk in audio_data:
                    audio_bytes += chunk

            # Transcribe the collected audio
            return await self.transcribe_audio(audio_bytes)
        except Exception as e:
            return f"Error processing audio stream: {str(e)}" 
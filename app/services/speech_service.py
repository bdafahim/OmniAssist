import whisper
import tempfile
import os
import logging
import ssl
import urllib.request
import urllib.error
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SpeechService")

class SpeechService:
    def __init__(self):
        self.model = None
        self.model_name = settings.WHISPER_MODEL
        logger.info(f"Initialized SpeechService with model: {self.model_name}")
        
        # Check if we should disable SSL verification
        self.disable_ssl_verify = os.environ.get("DISABLE_SSL_VERIFY", "false").lower() == "true"
        if self.disable_ssl_verify:
            logger.warning("SSL verification is disabled. This is not recommended for production.")
            ssl._create_default_https_context = ssl._create_unverified_context

    def _load_model(self):
        """
        Load the Whisper model lazily with enhanced error handling
        """
        if self.model is None:
            try:
                logger.info(f"Attempting to load Whisper model: {self.model_name}")
                
                # Check if model is already downloaded
                model_path = os.path.expanduser(f"~/.cache/whisper/{self.model_name}.pt")
                if os.path.exists(model_path):
                    logger.info(f"Model file found at: {model_path}")
                    logger.info(f"File size: {os.path.getsize(model_path) / (1024*1024):.2f} MB")
                else:
                    logger.info(f"Model file not found at: {model_path}, will download")
                
                # Try to load the model
                self.model = whisper.load_model(self.model_name)
                logger.info(f"Successfully loaded Whisper model: {self.model_name}")
                
            except ssl.SSLCertificateError as e:
                logger.error(f"SSL Certificate Error: {str(e)}")
                logger.error("This is likely due to a self-signed certificate in the certificate chain")
                logger.error("Consider setting environment variable: DISABLE_SSL_VERIFY=true (not recommended for production)")
                print(f"Warning: Could not load Whisper model due to SSL certificate error: {str(e)}")
                print("Using placeholder transcription service")
                
            except urllib.error.URLError as e:
                logger.error(f"URL Error: {str(e)}")
                logger.error("This could be due to network connectivity issues or proxy settings")
                print(f"Warning: Could not load Whisper model due to URL error: {str(e)}")
                print("Using placeholder transcription service")
                
            except Exception as e:
                logger.error(f"Unexpected error loading Whisper model: {str(e)}", exc_info=True)
                print(f"Warning: Could not load Whisper model: {str(e)}")
                print("Using placeholder transcription service")

    async def transcribe_audio(self, audio_data: bytes) -> str:
        """
        Transcribe audio data to text using Whisper
        """
        try:
            logger.info(f"Transcribing audio data of length: {len(audio_data)} bytes")
            
            # Create a temporary file to store the audio data
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(audio_data)
                temp_audio_path = temp_audio.name
                logger.info(f"Created temporary audio file: {temp_audio_path}")

            # Load model if not loaded
            self._load_model()

            if self.model is not None:
                # Transcribe the audio file
                logger.info(f"Transcribing audio file: {temp_audio_path}")
                result = self.model.transcribe(temp_audio_path)
                text = result["text"]
                logger.info(f"Transcription result: {text}")
            else:
                # Placeholder response if model is not available
                logger.warning("Model not available, using placeholder response")
                text = "I'm sorry, speech recognition is currently unavailable."

            # Clean up the temporary file
            os.unlink(temp_audio_path)
            logger.info(f"Deleted temporary audio file: {temp_audio_path}")

            return text
        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}", exc_info=True)
            return f"Error transcribing audio: {str(e)}"

    async def process_audio_stream(self, audio_data):
        """
        Process audio data from either a stream or a list of chunks
        """
        try:
            logger.info("Processing audio stream")
            
            # If audio_data is a list, concatenate the chunks
            if isinstance(audio_data, list):
                logger.info(f"Processing list of {len(audio_data)} audio chunks")
                audio_bytes = b"".join(audio_data)
            else:
                # If it's an async iterator, collect all chunks
                logger.info("Processing async iterator of audio chunks")
                audio_bytes = b""
                async for chunk in audio_data:
                    audio_bytes += chunk

            logger.info(f"Collected {len(audio_bytes)} bytes of audio data")
            
            # Transcribe the collected audio
            return await self.transcribe_audio(audio_bytes)
        except Exception as e:
            logger.error(f"Error processing audio stream: {str(e)}", exc_info=True)
            return f"Error processing audio stream: {str(e)}" 
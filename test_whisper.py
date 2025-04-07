import os
import whisper
import logging
import ssl
import urllib.request
import urllib.error

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("WhisperTest")

def test_whisper_loading():
    """
    Test loading the Whisper model with different SSL verification settings
    """
    model_name = "base"  # Use a small model for testing
    
    # Test 1: Default settings
    logger.info("Test 1: Loading with default SSL verification")
    try:
        model = whisper.load_model(model_name)
        logger.info(f"Successfully loaded model: {model_name}")
    except Exception as e:
        logger.error(f"Failed to load model with default settings: {str(e)}")
    
    # Test 2: Disable SSL verification
    logger.info("Test 2: Loading with SSL verification disabled")
    try:
        # Create an unverified context
        ssl._create_default_https_context = ssl._create_unverified_context
        
        # Try loading again
        model = whisper.load_model(model_name)
        logger.info(f"Successfully loaded model with SSL verification disabled: {model_name}")
    except Exception as e:
        logger.error(f"Failed to load model with SSL verification disabled: {str(e)}")
    
    # Test 3: Check model cache
    logger.info("Test 3: Checking model cache")
    cache_dir = os.path.expanduser("~/.cache/whisper")
    model_path = os.path.join(cache_dir, f"{model_name}.pt")
    
    if os.path.exists(model_path):
        logger.info(f"Model file exists at: {model_path}")
        logger.info(f"File size: {os.path.getsize(model_path) / (1024*1024):.2f} MB")
    else:
        logger.info(f"Model file does not exist at: {model_path}")
    
    # Test 4: Check network connectivity
    logger.info("Test 4: Checking network connectivity")
    try:
        # Try to connect to OpenAI's website
        response = urllib.request.urlopen("https://openai.com", timeout=5)
        logger.info(f"Network connectivity OK: {response.getcode()}")
    except Exception as e:
        logger.error(f"Network connectivity issue: {str(e)}")

if __name__ == "__main__":
    logger.info("Starting Whisper model loading test")
    test_whisper_loading()
    logger.info("Test completed") 
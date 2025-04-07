import os
import ssl
import urllib.request
import tempfile
import shutil
from pathlib import Path

def download_whisper_model():
    # Create a custom SSL context that doesn't verify certificates
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Model URL and local path
    model_name = "base"
    model_url = f"https://openaipublic.azureedge.net/main/whisper/models/81f7c96c852ee8f8320b31b2b3b26facc42fdd487f06f95d32e35e0fcc54a9a9/{model_name}.pt"
    
    # Create cache directory if it doesn't exist
    cache_dir = Path.home() / ".cache" / "whisper"
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    model_path = cache_dir / f"{model_name}.pt"
    
    if model_path.exists():
        print(f"Model already exists at {model_path}")
        return str(model_path)
    
    print(f"Downloading Whisper {model_name} model...")
    
    try:
        # Download to a temporary file first
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            with urllib.request.urlopen(model_url, context=ssl_context) as response:
                shutil.copyfileobj(response, temp_file)
        
        # Move the temporary file to the final location
        shutil.move(temp_file.name, model_path)
        print(f"Model downloaded successfully to {model_path}")
        return str(model_path)
    
    except Exception as e:
        print(f"Error downloading model: {str(e)}")
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)
        raise

if __name__ == "__main__":
    try:
        model_path = download_whisper_model()
        print(f"Model is ready at: {model_path}")
    except Exception as e:
        print(f"Failed to download model: {str(e)}") 
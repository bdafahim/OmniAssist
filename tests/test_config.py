import os
import sys

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings

def test_config():
    print("Testing Configuration")
    print("-" * 50)
    print(f"Project Name: {settings.PROJECT_NAME}")
    print(f"API Version: {settings.API_V1_STR}")
    print(f"Business Type: {settings.BUSINESS_TYPE}")
    print(f"Whisper Model: {settings.WHISPER_MODEL}")
    print(f"Language Model: {settings.LANGUAGE_MODEL}")
    print("-" * 50)

if __name__ == "__main__":
    test_config() 
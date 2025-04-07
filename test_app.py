import uvicorn
import os
import sys

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("Starting the AI Customer Service & Ordering Agent...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000) 
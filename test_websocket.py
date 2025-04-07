import asyncio
import websockets
import json
import wave
import sys

async def test_websocket():
    uri = "ws://localhost:8000/api/v1/voice/ws"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket server")
            
            # Open and read the audio file
            try:
                with wave.open("test.wav", 'rb') as wave_file:
                    # Read the entire audio file
                    audio_data = wave_file.readframes(wave_file.getnframes())
                    
                    print(f"Sending {len(audio_data)} bytes of audio data...")
                    
                    # Send the audio data
                    await websocket.send(audio_data)
                    
                    # Wait for and print the response
                    response = await websocket.recv()
                    response_data = json.loads(response)
                    print("\nServer response:")
                    print(json.dumps(response_data, indent=2))
                        
            except FileNotFoundError:
                print("Error: test.wav file not found. Please create it first.")
            except Exception as e:
                print(f"Error processing audio: {str(e)}")
    
    except websockets.exceptions.ConnectionRefusedError:
        print("Error: Could not connect to the WebSocket server. Is the server running?")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    print("Starting WebSocket test...")
    asyncio.run(test_websocket()) 
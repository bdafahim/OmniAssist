import wave
import struct
import math
import numpy as np

def create_test_audio(filename="test.wav", duration=3, frequency=440, sample_rate=16000):
    """
    Create a test WAV file with a simple tone.
    
    Args:
        filename (str): Output WAV file name
        duration (float): Duration in seconds
        frequency (float): Frequency of the tone in Hz
        sample_rate (int): Sample rate in Hz
    """
    # Calculate number of frames
    n_frames = int(duration * sample_rate)
    
    # Generate time array
    t = np.linspace(0, duration, n_frames, False)
    
    # Generate sine wave
    tone = np.sin(2 * np.pi * frequency * t)
    
    # Convert to 16-bit PCM
    audio_data = (tone * 32767).astype(np.int16)
    
    # Create WAV file
    with wave.open(filename, 'w') as wav_file:
        # Set parameters
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        
        # Write audio data
        wav_file.writeframes(audio_data.tobytes())
    
    print(f"Created test audio file: {filename}")
    print(f"Duration: {duration} seconds")
    print(f"Frequency: {frequency} Hz")
    print(f"Sample rate: {sample_rate} Hz")

if __name__ == "__main__":
    create_test_audio() 
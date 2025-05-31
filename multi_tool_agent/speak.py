import requests
import pygame
import time
from pydub import AudioSegment
from pydub.playback import play
import base64
import requests
import os

# Set your API key
API_KEY = os.getenv("GEMINI_API_KEY")

# Define the text to convert to speech
TEXT = "Hello, Kritik! Welcome to AI-powered speech synthesis."

def text_to_speech(TEXT):
    LANGUAGE_CODE = "en-US"
    VOICE_NAME = "en-US-Wavenet-D"
    AUDIO_ENCODING = "LINEAR16"  # WAV format

    # Define the API endpoint
    URL = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={API_KEY}"

    # Prepare the request payload
    payload = {
        "input": {"text": TEXT},
        "voice": {"languageCode": LANGUAGE_CODE, "name": VOICE_NAME},
        "audioConfig": {"audioEncoding": AUDIO_ENCODING}
    }

    # Send the request
    response = requests.post(URL, json=payload)

    # Process the response
    if response.status_code == 200:
        audio_content = response.json()["audioContent"]
        
        # Decode Base64-encoded audio content and save the file
        audio_file = "output.wav"
        with open(audio_file, "wb") as file:
            file.write(base64.b64decode(audio_content))

        audio = AudioSegment.from_file("output.wav")
        play(audio)    # Play the audio using pydub

    else:
        print(f"Error: {response.status_code}, {response.text}")


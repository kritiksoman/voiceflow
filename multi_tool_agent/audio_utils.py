import numpy as np
import io
import wave
from google import genai
import os
from scipy.io import wavfile
import tempfile


def numpy_to_temp_wav(audio_array: np.ndarray, sample_rate: int) -> str:
    """Convert NumPy audio array to a temporary WAV file."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    
    with wave.open(temp_file.name, "wb") as wav_file:
        wav_file.setnchannels(1)  # Assuming mono audio
        wav_file.setsampwidth(2)  # Assuming 16-bit PCM audio
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_array.astype(np.int16).tobytes())

    return temp_file.name


def transcribe_audio(audio_array: np.ndarray, sample_rate: int, instruction:str):
    """Transcribe NumPy audio array using Google Gemini API."""
    temp_audio_path = numpy_to_temp_wav(audio_array, sample_rate)

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    myfile = client.files.upload(file=temp_audio_path)

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=[instruction, myfile]
    )

    return response.text


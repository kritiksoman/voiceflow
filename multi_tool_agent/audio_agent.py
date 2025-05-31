import sounddevice as sd
import numpy as np
from pydub import AudioSegment
from pydub.silence import detect_silence
from scipy.io.wavfile import write
from multi_tool_agent.audio_utils import transcribe_audio
from multi_tool_agent.ocr_agent import ocr_agent
from multi_tool_agent.terminal_agent import terminal_agent
from multi_tool_agent.type_agent import keyboard_agent
# from voice_agent import speak
# from agents import Agent, HandoffInputData, Runner, function_tool, handoff, trace
# from text_agent import first_agent
import asyncio
from google import genai
import os
import json
from multi_tool_agent.speak import text_to_speech


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
                

async def is_silent(audio_data, samplerate, silence_threshold=-40, min_silence_duration=500):
    """
    Detect silence using pydub and determine if audio is silent.
    
    Args:
        audio_data (np.ndarray): The recorded audio as a NumPy array.
        samplerate (int): The sampling rate in Hz.
        silence_threshold (int): Silence threshold in dBFS.
        min_silence_duration (int): Minimum silence duration in milliseconds.
    
    Returns:
        bool: True if silence is detected, False otherwise.
    """
    # Convert NumPy array to pydub AudioSegment
    audio_segment = AudioSegment(
        audio_data.tobytes(),
        frame_rate=samplerate,
        sample_width=audio_data.dtype.itemsize,
        channels=1
    )
    silence_ranges = detect_silence(
        audio_segment,
        min_silence_len=min_silence_duration,
        silence_thresh=silence_threshold
    )
    end = int(1000*len(audio_data)/samplerate)
    # return len(silence_ranges) > 0 
    if len(silence_ranges) > 0 and silence_ranges[0][0] == 0 and silence_ranges[0][1] == end:
        return False
    elif len(silence_ranges) > 1  and silence_ranges[-1][1] == end:
        return True
    else:
        return False
    
async def record_until_silence_async(samplerate=44100, chunk_duration=1, silence_threshold=-40, min_silence_duration=500):
    """
    Asynchronously record audio and stop when silence is detected.
    
    Args:
        samplerate (int): Sampling rate in Hz.
        chunk_duration (int): Duration of each chunk in seconds.
        silence_threshold (int): Silence threshold in dBFS.
        min_silence_duration (int): Minimum silence duration in milliseconds.
    
    Returns:
        np.ndarray: Recorded audio up to the silence point.
    """
    print("Recording... Speak into the microphone.")
    
    chunk_size = int(chunk_duration * samplerate)
    audio_buffer = np.array([], dtype='int16')
    i = 0
    with sd.InputStream(samplerate=samplerate, channels=1, dtype='int16') as stream:
        while True:
            # Read audio asynchronously
            chunk, _ = await asyncio.to_thread(stream.read, chunk_size)
            audio_buffer = np.concatenate((audio_buffer, chunk.flatten()))
            
            # Check for silence asynchronously
            if await is_silent(audio_buffer, samplerate, silence_threshold, min_silence_duration):
                print("Silence detected. Stopping recording.")
                # await speak(audio_buffer)
                # await save_audio_as_wav(audio_buffer, samplerate, str(i) + ".wav")
                commands = transcribe_audio(audio_buffer, samplerate, instruction="Transcribe the audio to text, break it into steps, identify if the user wants to click or run a terminal command. Return the output as a list of dictionaries with the same keys in the format: [{'instruction': '', 'command':'click or terminal or None or type'}].\nInstructions for commands: If the user says 'click', it is a click command. If the user says 'type' or 'press', it is a type command. Otherwise, if the user says 'run', 'open', 'close', 'execute', it is a terminal command.  \nAudio input: ")
                print("Command detected : ", commands)
                s = commands.find("[")
                e = commands.find("]")
                js = commands[s:e+1].replace("'", '"')
                # js = repair_json(action_response.text[s:e+1])
                commands = json.loads(js)
                try:
                    for command in commands:
                        if command['command'] == 'click':
                            print("Clicking on the button: ", command['instruction'])
                            ocr_agent(command['instruction'])
                        elif command['command'] == 'terminal':
                            print("Running terminal command: ", command['instruction'])
                            terminal_agent(command['instruction'])
                        elif command['command'] == 'type':
                            print("Running type command: ", command['instruction'])
                            keyboard_agent(command['instruction'])
                        else:
                            text_to_speech("Sorry, I could not process the command. Please try again.")
                            break
                except Exception as e:
                    print(e)
                    text_to_speech("Sorry, I could not process the command. Please try again.")
                # action_response = client.models.generate_content(
                # model="gemini-2.0-flash",
                # contents=f"Parse the user input to identify if the user wants to click or run a terminal command. \nUser input: {command}\n")
                # result = await Runner.run(first_agent, input=command)
                # print("Result : ", result.final_output)
                audio_buffer = np.array([], dtype='int16')
                i += 1
                # break
    return
    # return audio_buffer

async def save_audio_as_wav(audio_data, samplerate, output_filename):
    """
    Asynchronously save audio data as a .wav file.
    
    Args:
        audio_data (np.ndarray): The recorded audio data.
        samplerate (int): Sampling rate in Hz.
        output_filename (str): Filename for the output audio file.
    """
    await asyncio.to_thread(write, output_filename, samplerate, audio_data)
    print(f"Audio saved as '{output_filename}'")


async def track_audio():
    print("Starting Voiceflow...")
    # Parameters
    samplerate = 24000 #44100
    silence_threshold = -40
    min_silence_duration = 500
    # output_filename = "output_audio_async.wav"

    # Record audio asynchronously until silence
    audio_data = await record_until_silence_async(
        samplerate=samplerate,
        silence_threshold=silence_threshold,
        min_silence_duration=min_silence_duration
    )
    

if __name__ == "__main__":
    asyncio.run(track_audio())

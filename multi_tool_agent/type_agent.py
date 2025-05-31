import time
import pyautogui
from google import genai
import os
from multi_tool_agent.speak import text_to_speech

API_KEY = os.getenv("GEMINI_API_KEY")

instruction = "Press cmd + c"

def keyboard_agent(instruction):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    action_response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Perform instruction of the user by a python script which only calls autopygui functions like pyautogui.keyDown('shift'), pyautogui.press('a'), pyautogui.keyUp('shift'), pyautogui.hotkey('ctrl', 's') to perform the action. The script should be enclosed in ```.'} \n The JSON should be valid.\n User input: " + instruction + "\n .",
    )
    command = ""
    try:
        # print(action_response.text)

        s = action_response.text.find("```")
        e = action_response.text.rfind("```")

        js = action_response.text[s+3:e].strip()
        # js = repair_json(action_response.text[s:e+1])
        command = js #json.loads(js)
        # run the script
        
        if command.startswith("python"):
            command = command[6:].strip()
        print(command)
        # if 'script' in command:
        exec(command)
        # elif 'type' in command:
        #     pyautogui.typewrite(command['type'])
        # elif 'llm' in command:
        #     pyautogui.typewrite(command['llm'])
        print("\n Executed the script successfully.")
    except Exception as e:
        print(f"Error executing command: {e}")
        text_to_speech("Sorry, I could not type your command. Please try again.")

if __name__ == "__main__":
    # keyboard_agent("type a llm generated story about clowns in 150 words")
    keyboard_agent("type control plus c")

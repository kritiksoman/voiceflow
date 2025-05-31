import asyncio
import os
os.environ["GEMINI_API_KEY"] = "" #TODO: enter your API key here
import rumps
import multiprocessing
from multi_tool_agent.audio_agent import track_audio


def run_audio():
    asyncio.run(track_audio())  # Properly handle the async function


class MyApp(rumps.App):
    def __init__(self):
        super().__init__("VoiceFlow")  # App name in the menu bar
        self.process = None  # Track the process
        self.menu = ["Start/Pause Tracking Audio"]

    @rumps.clicked("Start/Pause Tracking Audio")
    def change_state(self, _):
        if self.process and self.process.is_alive():
            self.process.terminate()
            self.process = None  # Reset the reference after termination
        else:
            self.process = multiprocessing.Process(target=run_audio, daemon=True)
            self.process.start()


if __name__ == "__main__":
    MyApp().run()

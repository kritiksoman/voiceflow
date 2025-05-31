from AppKit import NSWorkspace
import subprocess
import platform

import pyautogui
system_name = platform.system()
import numpy as np
import io
import soundfile as sf
import os



def set_current_window(window_name: str)-> None:
    """
    Set the current window to the given window name."""
    if system_name != "Darwin":
        print("System is not macOS, cannot set window.")
    else:
        # if window_name.endswith(".app"):
        #     print("Opening window... {}".format(window_name))
        #     apple_script = f'do shell script "open " & quoted form of "{window_name}"'
        #     # Run AppleScript
        #     subprocess.run(["osascript", "-e", apple_script])
        # else:
        sc_w, sc_h = pyautogui.size()
        apple_script = '''tell application "{window_name}" 
        activate 
        delay 1 -- Allow time for the app to open
        tell application "System Events"
            set frontApp to (first application process whose frontmost is true)
            tell frontApp
                set frontWindow to (first window)
                set frontWindow's size to {sc_w, sc_h} -- Adjust based on screen resolution
                set frontWindow's position to {0, 0}
            end tell
        end tell
        end tell'''.replace("{window_name}", window_name).replace("sc_w", str(sc_w)).replace("sc_h", str(sc_h))
        subprocess.run(["osascript", "-e", apple_script])
    return


def close_given_window(window_name: str)-> None:
    """
    Close the given window name."""
    if system_name != "Darwin":
        print("System is not macOS, cannot set window.")
    else:
        if window_name.endswith(".app"):
            print("Converting name... {}".format(window_name))
            apple_script = f'tell application "{window_name}" to get its name'
            # Run AppleScript
            window_name = subprocess.run(["osascript", "-e", apple_script], capture_output=True, text=True)
            window_name = window_name.stdout.strip()
        print("Closing window... {}".format(window_name))
        apple_script = f'tell application "{window_name}" to quit'
        subprocess.run(["osascript", "-e", apple_script])
    return
import pygetwindow as gw
import pyautogui
import win32com.client

speaker = win32com.client.Dispatch("SAPI.SpVoice")


def say(text, rate=-1):
    speaker.Rate = rate
    speaker.speak(text)


def close_window(window_title):
    try:
        # Get all windows with the specified title
        windows = gw.getWindowsWithTitle(window_title)

        if windows:
            # Bring the first matching window to the front
            windows[0].activate()

            # Send the Alt + F4 keyboard shortcut to close the window
            pyautogui.hotkey('alt', 'f4')
            say(f"Window '{window_title}' closed.")
        else:
            say(f"Window '{window_title}' not found. or this is minimized position")
    except:
        pass

# Example: Close Notepad
# notepad_title = "whatsapp"
# close_window(notepad_title)

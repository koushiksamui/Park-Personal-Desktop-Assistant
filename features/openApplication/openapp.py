import time
import pyautogui
import win32com.client

speaker = win32com.client.Dispatch("SAPI.SpVoice")


def say(text, rate=-1):
    speaker.Rate = rate
    speaker.speak(text)


def openapp(quary):
    try:
        say(f"opening {quary} sir..")
        pyautogui.hotkey('win', 's')
        time.sleep(.8)
        pyautogui.typewrite(quary)
        time.sleep(2)
        # pyautogui.click(x=607, y=453)
        pyautogui.press('enter')
    except Exception as e:
        # If there's an exception, print an error message
        print(f"Error: {e}")
        say("Sorry, sir")



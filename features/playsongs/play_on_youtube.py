
import win32com.client
import webbrowser as wb
import time
import pyautogui

speaker = win32com.client.Dispatch("SAPI.SpVoice")


def say(text, rate=-1):
    speaker.Rate = rate
    speaker.speak(text)


def playYoutube(query):
    query = query.replace("park", "")
    query = query.replace(" on", "")
    query = query.replace("youtube", "")
    query = query.replace("search", "")
    query = query.replace("YouTube", "")
    query = query.replace("play", "")
    web = "https://www.youtube.com/results?search_query=" + query
    wb.open(web)
    time.sleep(5)
    pyautogui.click(x=645, y=296)
    say("done sir, playing first result")

import os
import win32com.client
import webbrowser as wb
from Body import Listen
from googlesearch import search
import datetime
from features.Chatbot.openAI_chatbot import reply_chat
import time
import pyautogui
from features.connect_with_mobile import connect
import psutil  # use for check charge computer
from features.playsongs import play_songs  # for songs play
from features.playsongs import play_on_youtube
import re
from features.openApplication import openapp
from features.volume_control.volume import volumeAdjust
from features.windows_features_on_off import close_window
from features.Image_Generation.AI_image import generate_image
import socket


speaker = win32com.client.Dispatch("SAPI.SpVoice")


def say(text, rate=-1):
    speaker.Rate = rate
    speaker.speak(text)


def mainExecution():
    wellcomeTime = datetime.datetime.now().strftime("%H.%M")

    if "06.00" <= wellcomeTime < "12.00":
        say("good morning sir.")
    elif wellcomeTime == "12.00":
        say("good noon sir.")
    elif "12.00" < wellcomeTime < "18.00":
        say("good afternoon sir.")
    elif "18.00" <= wellcomeTime < "21.00":
        say("good evening sir.")
    else:
        say("wellcome sir.")

    previous_response = ""
    previous_query = ""
    flag = 1
    while True:
        query = Listen.MicExecution()
        # ******************************This r task Execution*********************************************
        if "open google" in query.lower():
            wb.open("www.google.com")
            say("lunching google...")
            time.sleep(2)
            say("Anything else sir ...")
        elif "search youtube" in query.lower() or "search on youtube" in query.lower() or "on youtube" in query.lower():
            if flag == 1:
                flag = 0
            say("okay sir")
            play_on_youtube.playYoutube(query)
        elif "open website" in query.lower() or "show news" in query.lower() or "match update" in query.lower() or "search" in query.lower():
            query = query.replace("open site", "")
            query = query.replace("show news", "")
            query = query.replace("match update", "")
            query = query.replace("search", "")
            for j in search(query, tld="co.in", num=10, stop=1, pause=2):
                say(f"Opening {query}  ...")
                wb.open(j)
                say("Anything else sir ...")
        elif "open application" in query.lower():
            query = query.replace("Park", "")
            query = query.replace("open", "")
            query = query.replace("application", "")
            openapp.openapp(query)
            say("anything sir")
        elif "play song" in query.lower() or "play the song" in query.lower() or "play any song" in query.lower() or "play any songs" in query.lower() or "playlist" in query.lower():
            if "play song" in query.lower() or "play the song" in query.lower() or "play any song" in query.lower() or "play any songs" in query.lower():
                say("sir what song should i play")
                song = Listen.MicExecution()
                play_songs.play_songs(song)
            elif "playlist" in query.lower():
                # from features.playsongs.play_songs import playlist_chat
                reply_from_playlist = play_songs.playlist_chat(query)
                say(reply_from_playlist)
        elif "connect my phone" in query.lower():
            say("okay sir, try to connect your Phone..")
            connect.connectMobile()
            say("sir disconnect your phone")
        elif "create image" in query.lower():
            try:
                query = query.replace("create image", "").strip()
                print("wait few seconds")
                say("wait few seconds")
                generate_image(query)
                say("image created")
            except:
                say("sorry sir ..")
        elif "time now" in query:
            strTime = datetime.datetime.now().strftime("%H:%M")
            say(f"sir time is {strTime} now")
        elif "delete the chat log" in query.lower() or "delete chat log" in query.lower() or "clear chat log" in query.lower():
            say("sir it is an important file.there is had your previous saved data ......are you sure you can "
                "delete"
                "this file , yes or No ?")
            worn = Listen.MicExecution()
            if "yes" in worn.lower():
                f = open("chat_log.txt", "w")
                f.write("")
                print("clearing the logfile....")
                time.sleep(5)
                say("done sir. all deleted")
            else:
                say("sorry not delete the chat log, thankyou sir..")
        elif "show text" in query.lower():
            query = query.replace("show text", "")
            result = reply_chat(query)
            print(result)
        elif "save data" in query.lower():
            if not os.path.exists("C:\\Users\\samui\\Desktop\\ai respond save data"):
                os.mkdir("C:\\Users\\samui\\Desktop\\ai respond save data")
            if previous_response != "":
                # Create a text string with both the previous and current responses
                text = f"OpenAI Response for prompt :\n***************************************************\n\n"
                text += previous_response
                with open(f"C:\\Users\\samui\\Desktop\\ai respond save data/{''.join(previous_query)}.txt", "w") as f:
                    f.write(text)
                    say("done sir")
            query = query.replace("save", "")
            query = query.replace("data", "")
            if query.strip() != '':
                reply = reply_chat(query)
                print(reply)
                # Create a text string current responses
                text = f"OpenAI Response for prompt :\n***************************************************\n\n"
                text += reply
                with open(f"C:\\Users\\samui\\Desktop\\ai respond save data/{''.join(query)}.txt", "w") as f:
                    f.write(text)
                say("saved it..")
        elif "shut down my computer" in query.lower() or "shutdown my computer" in query.lower() or "shutdown computer" in query.lower():
            say("shutting down your computer sir..")
            os.system("shutdown /s /t 2")
        elif "restart my computer" in query.lower() or "restart computer" in query.lower():
            say("okay sir i will restart your computer..")
            os.system("shutdown /r /t 2")
        elif "log out my computer" in query.lower() or "log out computer" in query.lower():
            say("okay sir ..")
            os.system("shutdown /l ")
        elif "charge on my computer" in query.lower() or "charge status" in query.lower() or "battery status" in query.lower():
            battery = psutil.sensors_battery()
            if battery is None:
                print("No battery found.")
                exit()
            percentage = battery.percent
            print(f"Battery Percentage: {percentage}%")
            say(f"sir Battery {percentage} percentage are available now ")
        elif "give me prompt" in query.lower():
            query = input("You: ")
            reply = reply_chat(query)
            print(reply)
            say(reply)
        elif "volume" in query.lower() or "current volume" in query.lower():
            vol = volumeAdjust(query)
            print(vol)
            say(vol)
        elif "what is my ip" in query.lower():
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            print(ip)
            say(f"your ip address is {ip} ")
        elif "pause" in query.lower() or "resume" in query.lower() or "play" in query.lower():
            pyautogui.hotkey('playpause')
        elif "page down" in query.lower():
            pyautogui.hotkey('pagedown')
        elif "page up" in query.lower():
            pyautogui.hotkey('pageup')
        elif "close this" in query.lower() or "close window" in query.lower():
            say("closing sir..")
            pyautogui.hotkey('alt', 'f4')
        elif "close" in query.lower() or "exit" in query.lower():
            query = query.replace("close", "")
            query = query.replace("exit", "")
            close_window.close_window(query)
        elif "quit" in query.lower():
            if ("21.00" <= wellcomeTime <= "24.00") or ("01.00" <= wellcomeTime < "05.00"):
                say("bye,good night sir..")
            else:
                say("bye sir, thank you ")
            clearfile = open("chat_log.txt", "w")
            clearfile.write("")
            exit()
        elif "stop park" in query.lower() or "stop answer" in query.lower():
            if flag == 0:
                say("answer mode already stopped.")
            else:
                flag = 0
                say("okay sir. answer mode stopped now.")
        elif "hello park" in query.lower() or "ready for answer" in query.lower():
            flag = 1
            say("hello sir ")
        elif "minimise window" in query.lower() or "minimise this" in query.lower():
            pyautogui.hotkey('win', 'm')
        else:
            try:
                if flag == 1:
                    reply = reply_chat(query)
                    print(reply)
                    say(reply)
                    previous_response = reply
                    previous_query = query
                    if "https://www." in reply:
                        # Define a regular expression pattern to match URLs
                        url_pattern = re.compile(r'https?://\S+')
                        matches = re.findall(url_pattern, reply)
                        # Print the matched URLs
                        for match in matches:
                            say("lunching this..")
                            wb.open(match)
            except Exception as e:
                print(f"Response error : {e}")
                say("sorry sir. retry please")


if __name__ == "__main__":
    mainExecution()

from time import sleep
import re
import pyautogui
import win32com.client
from Ai_brain.Openai import generate_response
from Body.Listen import MicExecution
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pathlib
import warnings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from features.volume_control.volume import volumeAdjust

warnings.simplefilter("ignore")

ScriptDir = pathlib.Path().absolute()
url = "https://open.spotify.com/search/"
chrome_option = Options()
chrome_option.headless = False
chrome_option.add_argument('--profile-directory=Default')
chrome_option.add_argument(f'user-data-dir={ScriptDir}\\chromedata')
service = Service(ChromeDriverManager().install())

speaker = win32com.client.Dispatch("SAPI.SpVoice")


# load_dotenv()
# completion = openai.Completion()


def say(text, rate=-1):
    speaker.Rate = rate
    speaker.speak(text)


def Search_song(song, driver):
    Xpath_1 = "/html/body/div[4]/div/div[2]/div[3]/header/div[3]/div/div/form/input"

    try:
        sleep(1)
        # Wait for the popup to appear (adjust the timeout as needed)
        dismiss_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div[4]/button"))
        )

        # Click the dismiss button to close the popup
        dismiss_button.click()

    except TimeoutException:
        # Handle the case where the popup did not appear
        pass
    while True:
        try:
            driver.find_element(by=By.XPATH, value=Xpath_1)
            break
        except:
            pass
    driver.find_element(by=By.XPATH, value=Xpath_1).send_keys(song)


def Play_song(driver):
    Xpath_2 = "/html/body/div[4]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/div[2]/div/div/section[2]/div[2]/div/div/div/div[2]/div[1]/div/div[1]/div[1]/img"
    while True:
        try:
            driver.find_element(by=By.XPATH, value=Xpath_2)
            break
        except:
            pass
    driver.find_element(by=By.XPATH, value=Xpath_2).click()


def stop_resume_song(driver):
    Xpath_3 = "/html/body/div[4]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/button"
    driver.find_element(by=By.XPATH, value=Xpath_3).click()


def Chenge_Song(driver):
    Xpath_4 = "/html/body/div[4]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/div[2]/button[1]"
    driver.find_element(by=By.XPATH, value=Xpath_4).click()
    sleep(2)


def Previous_song(driver):
    Xpath_5 = "/html/body/div[4]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/div[1]/button[2]"
    driver.find_element(by=By.XPATH, value=Xpath_5).click()
    driver.find_element(by=By.XPATH, value=Xpath_5).click()
    sleep(2)


def mute_unmute_song(driver):
    Xpath_6 = "/html/body/div[4]/div/div[2]/div[2]/footer/div/div[3]/div/div[3]/button"
    driver.find_element(by=By.XPATH, value=Xpath_6).click()


def playlist_chat(query, chat_log=None):
    try:
        Filelog = open("songs_playlist.txt", "r")
        chat_log_template = Filelog.read()
        Filelog.close()
        if chat_log is None:
            chat_log = chat_log_template
        prompt = f'{chat_log} You: {query}\n '
        answer = generate_response(prompt)
        if "add" in query:
            try:
                chat_log_template_update = chat_log_template + f"\n{answer} "
                Filelog = open("songs_playlist.txt", "w")
                Filelog.write(chat_log_template_update)
                Filelog.close()
            except:
                say("sorry sir, not able to add any song")
        return answer
    except Exception as e:
        print(f"Response error : {e}")
        return "sorry sir, i am not able to response"


# Function to play songs based on user input
def play_songs(song):
    try:
        # Check if the user wants to stop playing songs
        if "don't play" in song.lower():
            say("okay sir,what do for you sir")
            return

        # Initialize the Chrome webdriver
        driver = webdriver.Chrome(service=service, options=chrome_option)
        driver.maximize_window()
        driver.get(url=url)

        # Check if the user wants to play a playlist or a specific song
        if "my playlist" in song.lower() or "any" in song.lower() or "your choice" in song.lower() or "you choice" in song.lower():

            # Get song suggestions through chat interaction
            songsplay = playlist_chat(f"Please suggest some songs related to this query '{song}'.Choose randomly and provide the song titles in double quotes.")
            # Use regular expression to find text within double quotes
            song_titles = re.findall(r'"([^"]*)"', songsplay)
            # Play the first suggested song
            say(f"okay sir, playing {song_titles[0]}, enjoy")
            Search_song(song_titles[0], driver)  # search song
            Play_song(driver)  # click song button
            while True:
                afterquery = MicExecution()

                if "exit the song" in afterquery.lower() or "exit song" in afterquery.lower() or "stop the song" in afterquery.lower() or "stop song" in afterquery.lower():
                    say("yes sir,")
                    print("yes sir")
                    pyautogui.click(x=1895, y=22)
                    return
                elif "pause song" in afterquery.lower() or "resume song" in afterquery.lower() or "pause the song" in afterquery.lower() or "resume the song" in afterquery.lower():
                    stop_resume_song(driver)
                elif "change song" in afterquery.lower() or "change the song" in afterquery.lower():
                    Chenge_Song(driver)
                elif "previous song" in afterquery.lower():
                    Previous_song(driver)
                elif "mute the song" in afterquery.lower() or "mute song" in afterquery.lower() or "unmute song" in afterquery.lower():
                    mute_unmute_song(driver)
                elif "volume" in afterquery.lower():
                    say("yes, setting the volume sir")
                    volumeAdjust(afterquery)
                elif "my playlist" in afterquery.lower():
                    try:
                        if "add this song" in afterquery.lower():
                            afterquery = afterquery.replace("this song", song_titles[0])
                            playlist_chat(afterquery)
                        else:
                            playlist_chat(afterquery)
                    except:
                        say("sorry sir ..")

        else:
            say(f"okay sir, playing {song}, enjoy")
            Search_song(song, driver)  # search song
            Play_song(driver)  # click song button
            while True:
                afterquery = MicExecution()

                if "exit the song" in afterquery.lower() or "exit song" in afterquery.lower() or "stop the song" in afterquery.lower() or "stop song" in afterquery.lower():
                    say("yes sir,")
                    print("yes sir")
                    pyautogui.click(x=1895, y=22)
                    return
                elif "pause song" in afterquery.lower() or "resume song" in afterquery.lower() or "pause the song" in afterquery.lower() or "resume the song" in afterquery.lower():
                    stop_resume_song(driver)
                elif "change song" in afterquery.lower() or "change the song" in afterquery.lower():
                    Chenge_Song(driver)
                elif "previous song" in afterquery.lower():
                    Previous_song(driver)
                elif "mute the song" in afterquery.lower() or "mute song" in afterquery.lower() or "unmute song" in afterquery.lower():
                    mute_unmute_song(driver)
                elif "volume" in afterquery.lower():
                    say("yes, setting the volume sir")
                    volumeAdjust(afterquery)
    except:
        say("sorry sir , try again")
        pyautogui.click(x=1895, y=22)

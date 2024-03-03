import re
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def get_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return volume.GetMasterVolumeLevelScalar()


def set_volume(level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(level, None)


def volumeAdjust(query):
    try:
        current_volume = get_volume()
        current_volume = int(current_volume * 100)
        print(f" Current volume is {current_volume}%")
        # Use a regular expression to find all numbers in the sentence
        numbers = [int(num) for num in re.findall(r'\d+', query)]
        if "increase" in query.lower() and numbers == []:
            if current_volume < 90:
                current_volume += 10
                set_volume(current_volume/100.0)
                return f"Adjusted the volume to increase by 10 times the current level."
            else:
                set_volume(100/100.0)
                return "Adjusted the volume full"
        elif "decrease" in query.lower() and numbers == []:
            if current_volume > 10:
                current_volume -= 10
                set_volume(current_volume/100.0)
                return f"Adjusted the volume to decrease by 10 times the current level."
            else:
                set_volume(1/100.0)
                return "Adjusted the volume 1"
        else:
            # Loop through the extracted numbers
            for number in numbers:
                # Adjust the volume to the specified level
                set_volume(number / 100.0)  # Assuming volume values are in the range 0 to 100
                # For demonstration, let's print a message for each number
                return f"Adjusted volume to level {number}%."
    except:
        return "Sorry, unable to set volume."
    return f"Current volume is {current_volume}%."


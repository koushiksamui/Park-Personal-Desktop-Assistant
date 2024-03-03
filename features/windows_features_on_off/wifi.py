import subprocess
import platform

def turn_on_bluetooth():
    if platform.system().lower() == "windows":
        subprocess.run(["powershell", "Enable-WindowsOptionalFeature -Online -FeatureName Bluetooth -NoRestart"], capture_output=True, text=True)
        print("Bluetooth turned on.")
    else:
        print("This script is intended for Windows only.")

def turn_off_bluetooth():
    if platform.system().lower() == "windows":
        subprocess.run(["powershell", "Disable-WindowsOptionalFeature -Online -FeatureName Bluetooth -NoRestart"], capture_output=True, text=True)
        print("Bluetooth turned off.")
    else:
        print("This script is intended for Windows only.")

# Example usage
# turn_off_bluetooth()
# Do something that requires Bluetooth to be off
turn_on_bluetooth()
# Do something that requires Bluetooth to be on

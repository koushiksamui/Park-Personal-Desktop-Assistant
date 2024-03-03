import os
import socket
import pyautogui
import win32com.client
import webbrowser as wb

speaker = win32com.client.Dispatch("SAPI.SpVoice")


def say(text):
    speaker.speak(text)


def connectMobile():
    try:
        # Set up a socket server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', 12345))  # Use a specific port
        server_socket.listen(1)
        print("Listening for connections...")
        say("Sir, please run the client script on your mobile.")

        # Accept a connection from the smartphone
        client_socket, client_address = server_socket.accept()
        print(f"Connected to {client_address}")
        say("Connection successful, sir.")

        while True:
            command = client_socket.recv(1024).decode()

            if command == "move":
                # Receive X and Y coordinates for cursor movement
                x, y = client_socket.recv(1024).decode().split(',')
                x, y = int(x), int(y)
                pyautogui.moveTo(x, y)
            elif command == "click":
                # Simulate a mouse click
                pyautogui.click()
            elif command == "shut down":
                say("shut down your computer sir..")
                os.system("shutdown /s /t 1")
            elif command == "restart":
                say("restarting your computer sir..")
                os.system("shutdown /r /t 1")
            elif command == "open google":
                wb.open("www.google.com")
                client_socket.send(b"opened google.com")

            elif command == "exit":
                break

        client_socket.close()
        server_socket.close()

    except Exception as e:
        print(f"An error occurred: {e}")
        say("An error occurred. Please check the server script on your mobile.")

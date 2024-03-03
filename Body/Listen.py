import speech_recognition as sr


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listing....")
        audio = r.listen(source, 0, 10)
        try:
            print("Recognizing....")
            query = r.recognize_google(audio, language="en-IN")
            print(f"user said: {query}")
            return query
        except:
            pass


def MicExecution():
    query = takeCommand()
    # data = Translation(query)
    if query is None:
        return MicExecution()
    return query


# if __name__ == "__main__":
#     while True:
#         quary = MicExecution()
#         f = open("query.txt", "w")
#         f.write(quary)
#         f.close()

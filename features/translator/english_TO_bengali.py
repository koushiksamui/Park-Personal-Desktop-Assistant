
from googletrans import Translator
from plyer import notification


# -- Translator --

def Translation(Text):
   try:
        line = str(Text)
        translate = Translator()
        result = translate.translate(line, dest='bn')
        data = result.text
        print(f"bengali meaning {Text} is: {data}")
        return data
   except:
       pass


def Translate(query):
    data = Translation(query)
    notification.notify(title=query,
                        message=data, timeout=30)
    return data


# if __name__ == "__main__":
#     MicExecution()

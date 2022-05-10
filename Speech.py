import speech_recognition as sr

r = sr.Recognizer()

class Speech:
    def __init__(self):
        self.text = ""

    '''
    Update text by listening through laptop microphone
    '''
    def get_text(self):
        self.text = ""
        with sr.Microphone() as source:
            audio = r.listen(source)

            try:
                text = r.recognize_google(audio)
                self.text = text
                print(self.text)
            except:
                pass
        
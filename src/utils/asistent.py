import speech_recognition as sr
import pyttsx3

class Asistent:
    def __init__(self):
        self.r = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.text = None
        self.repiter()
        
    
    def asistent_init(self):
        voices = self.engine.getProperty("voices")
        self.engine.setProperty('rate', 150) 
        self.engine.setProperty('volume', 1.0)
        self.engine.setProperty("voice", voices[0].id)
        
    def repiter(self):
            with sr.Microphone() as source:
                while True:
                    try:
                        self.asistent_init()
                        self.engine.say("...")
                        audio = self.r.listen(source)
                        self.text = self.r.recognize_google(audio, language="es-ES")
                        self.engine.say(f"Dijiste {self.text}")
                        self.engine.runAndWait()
                        print(self.text)
                        if self.text == 'cerrar': 
                            break
                        
                    except sr.UnknownValueError:
                        print("No se entendio el audio")
                     
                    except Exception as e:
                        print('Hubo un error: ', e)

        
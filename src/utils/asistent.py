import speech_recognition as sr
import pyttsx3

class Asistent:
    def __init__(self):
        self.r = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.is_running = True
        self._setup_voice()
        
    
    def _setup_voice(self):
        voices = self.engine.getProperty("voices")
        self.engine.setProperty('rate', 150) 
        self.engine.setProperty('volume', 1.0)
        
        if voices:
            self.engine.setProperty("voice", voices[0].id)
    
    def talk(self, text):
        self.engine.say(text)
    
    def listen_from_microphone(self):
        try:
            with sr.Microphone() as source:
                audio = self.r.listen(source)
                text = self.r.recognize_google(audio, language="es-ES")
                print(text)
                return text
            
        except sr.UnknownValueError:
            print("No se entendio el audio")
                     
        except Exception as e:
            print('Hubo un error: ', e)
    
    def handle_command(self, command):
        comands_handlers = {
            'repetir': self.repiter_mode,
            'cerrar': self.close 
        }
        
        handler = comands_handlers.get(command)
        if handler:
            handler()
        else:
            self.talk("comando no reconocido")
    
    def close(self):
        self.talk("Hasta luego")
        self.is_running = False
    
    def repiter_mode(self):
        self.talk("Modo repetición activado. Di algo para repetirlo o 'salir' para salir.")
        while True:
            command = self.listen_from_microphone()
            self.talk('...')
            
            if command == "salir":
                self.talk("Saliendo del modo repetición")
                break
            elif command:
                self.talk(f"Dijiste: {command}")
            
            self.engine.runAndWait()
    
    def run(self):
        self.talk("Asistente activado. Elige funcionalidad.")
        self.talk("Opcion 1: repetir")
        self.talk("Opcion 2: cerrar")

        while self.is_running:
            self.engine.runAndWait()
            command = self.listen_from_microphone()
            self.engine.runAndWait()       
            if command:
                self.handle_command(command)
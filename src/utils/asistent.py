import speech_recognition as sr
import pyttsx3
from .apis.getDailyWord import get_daily_word

class Asistent:
    def __init__(self):
        self.r = sr.Recognizer()
        self.is_running = True
    
    def _setup_voice(self, engine):
        voices = engine.getProperty("voices")
        engine.setProperty('rate', 150) 
        engine.setProperty('volume', 1.0)
        
        if voices:
            engine.setProperty("voice", voices[0].id)
    
    def talk(self, text):
        engine = pyttsx3.init()
        self._setup_voice(engine)
        engine.say(text)
        engine.runAndWait()
        engine.stop() 
    
    def listen_from_microphone(self):
        with sr.Microphone() as source:
            try:
                self.r.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.r.listen(source, timeout=5)
                text = self.r.recognize_google(audio, language="es-ES")
                print(text)
                return text
            except sr.WaitTimeoutError:
                print("⏰ Timeout - No se detectó voz")
                return None
            except sr.UnknownValueError:
                print("No se entendio el audio")
                return None
            except Exception as e:
                print('Hubo un error: ', e)
    
    def handle_command(self, command):
        comands_handlers = {
            'repetir': self.repiter_mode,
            'adivinar': self.guess_word,
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
    
    def guess_word(self):
        try:
            self.talk("Modo adivinanza activado. adivina la palabra.")
            result = get_daily_word()
            word = result['data']['word']

            max_attempts = 5
            attempts = 0

            self.talk(f"La palabra tiene {len(word)} letras. ¡Comienza!")

            while attempts < max_attempts:
                command = self.listen_from_microphone()
                
                if command == 'salir':
                    self.talk('Saliendo del modo adivinanza')
                    return
                elif command == 'pista':
                    self._give_hint(word, attempts)
                    continue
                
                attempts += 1
                
                if command == word:
                    self.talk(f'¡Correcto! Adivinaste en {attempts} intentos!')
                    break
                else:
                    remaining = max_attempts - attempts
                    self.talk(f'Incorrecto. Te quedan {remaining} intentos.')
                    self._give_feedback(word, command, attempts)
                    
                if attempts >= max_attempts:
                    self.talk(f'Game over. La palabra era: {word}')
                    
        except Exception as e:
           print(f"error {e}")
    
    def _give_hint(self, palabra, attempt):
        hint_length = min(attempt + 1, len(palabra))
        hint = palabra[:hint_length]
        self.talk(f"Pista: la palabra empieza con {hint}")
    
    def _give_feedback(self, palabra, attempt, attempt_count):
        try:
            if len(attempt) != len(palabra):
                self.talk(f"La palabra tiene {len(palabra)} letras, no {len(attempt)}")
            else:
                correct_letters = sum(1 for a, b in zip(attempt, palabra) if a == b)
                self.talk(f"Tienes {correct_letters} letras correctas en la posición adecuada")
        except Exception as e:
            self.talk('Por favor diga algo')
        
    def repiter_mode(self):
        self.talk("Modo repetición activado. Di algo para repetirlo o 'salir' para salir.")
        while True:
            command = self.listen_from_microphone()
            
            if command == "salir":
                self.talk("Saliendo del modo repetición")
                break
            elif command:
                self.talk(f"Dijiste: {command}")
    
    def run(self):
        self.talk("Asistente activado. Elige funcionalidad.")
        self.talk("Opcion 1: repetir. Opcion 2: adivinar. Opcion 3: cerrar")
        
        while self.is_running:
            command = self.listen_from_microphone()
            if command:
                self.handle_command(command)
            else:
                self.talk("No entendí el comando. Las opciones son: repetir, adivinar o cerrar")

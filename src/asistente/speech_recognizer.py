import speech_recognition as sr

class SpeechRecognizer:
    def __init__(self, language="es-ES"):
        self.recognizer = sr.Recognizer()
        self.language = language
    
    def listen_from_microphone(self):
        with sr.Microphone() as source:
            try:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio, language=self.language)
                print(f"🎤 Reconocido: {text}")
                return text.lower()
            except sr.WaitTimeoutError:
                print("⏰ Timeout - No se detectó voz")
                return None
            except sr.UnknownValueError:
                print("❌ No se entendió el audio")
                return None
            except Exception as e:
                print(f'❌ Error en reconocimiento: {e}')
                return None

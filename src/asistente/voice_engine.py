import pyttsx3

class VoiceEngine:
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

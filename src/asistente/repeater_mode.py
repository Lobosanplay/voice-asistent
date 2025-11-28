class RepeaterMode:
    def __init__(self, voice_engine, speech_recognizer):
        self.voice_engine = voice_engine
        self.speech_recognizer = speech_recognizer
    
    def activate(self):
        self.voice_engine.talk("Modo repetición activado. Di algo para repetirlo o 'salir' para salir.")
        
        while True:
            command = self.speech_recognizer.listen_from_microphone()
            
            if command == "salir":
                self.voice_engine.talk("Saliendo del modo repetición")
                break
            elif command:
                self.voice_engine.talk(f"Dijiste: {command}")

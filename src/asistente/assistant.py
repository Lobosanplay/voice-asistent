from .voice_engine import VoiceEngine
from .speech_recognizer import SpeechRecognizer
from .word_game import WordGame
from .repeater_mode import RepeaterMode

class Assistant:
    def __init__(self):
        self.voice_engine = VoiceEngine()
        self.speech_recognizer = SpeechRecognizer()
        self.word_game = WordGame(self.voice_engine, self.speech_recognizer)
        self.repeater_mode = RepeaterMode(self.voice_engine, self.speech_recognizer)
        self.is_running = True
        
        self._setup_command_handlers()
    
    def _setup_command_handlers(self):
        self.command_handlers = {
            'repetir': self.repeater_mode.activate,
            'adivinar': self.word_game.start_game,
            'cerrar': self.close
        }
    
    def handle_command(self, command):
        handler = self.command_handlers.get(command)
        if handler:
            handler()
        else:
            self.voice_engine.talk("Comando no reconocido")
    
    def close(self):
        self.voice_engine.talk("Hasta luego")
        self.is_running = False
    
    def run(self):
        self.voice_engine.talk("Asistente activado. Elige funcionalidad.")
        self.voice_engine.talk("Opciones: repetir, adivinar o cerrar")
        
        while self.is_running:
            command = self.speech_recognizer.listen_from_microphone()
            if command:
                self.handle_command(command)
            else:
                self.voice_engine.talk("No entendí el comando. Las opciones son: repetir, adivinar o cerrar")

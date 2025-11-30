from .voice_engine import VoiceEngine
from .speech_recognizer import SpeechRecognizer
from .modes.word_game_mode.word_game import WordGame
from .modes.repeater_mode.repeater_mode import RepeaterMode
from dotenv import load_dotenv
import re 
import shutil
import os


load_dotenv()

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
            'adivinar': self.word_game.select_mode,
            'cerrar': self.close
        }
    
    def open_file(self, name):
        self.voice_engine.talk(f'Buscando el arhivo {name}')
        for key, value in os.environ.items():
            if name.upper() == key:
                self.voice_engine.talk(f'Abriendo {name}')
                os.startfile(value)
                return 
                 
            if name == 'all':
                for key, value in os.environ.items():
                    self.voice_engine.talk('Abriendo Todos las aplicaciones')
                    os.startfile(value)
                    return
    
        file_path = shutil.which(name)

        if file_path:
            print(file_path)
            self.voice_engine.talk(f'Abriendo {name}')
            os.startfile(file_path)
            return
        else: 
            self.voice_engine.talk('No se encontro la ruta del archivo')
    
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
        self.voice_engine.talk("Opciones: repetir, adivinar, abrir aplicaciion o cerrar")
        
        while self.is_running:
            command = self.speech_recognizer.listen_from_microphone()
            
            try:
                if not command.startswith('open'):
                    self.handle_command(command)
                elif command.startswith('open') or command.startswith('Open'):
                    file_name = re.sub("open ", "", command.lower())
                    self.open_file(file_name)
                else:
                    self.voice_engine.talk("No entendí el comando. Las opciones son: repetir, adivinar o cerrar")
            except Exception as e:
                self.voice_engine.talk('Porfavor diga algo')
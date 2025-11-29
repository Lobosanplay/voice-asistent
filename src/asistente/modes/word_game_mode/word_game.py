from ...utils.apis.modeGameWord import modeGameWord

class WordGame:
    def __init__(self, voice_engine, speech_recognizer):
        self.voice_engine = voice_engine
        self.speech_recognizer = speech_recognizer
        self.max_attempts = 5
        self.is_active = True
        
        self._mode_handlers()
    
    def _mode_handlers(self):
        self.command_handlers = {
            'random': self.start_game,
            'daily': self.start_game,
            'salir': self.exit
        }
    
    def select_mode(self):
        self.voice_engine.talk("Elige el modo del juego")
        self.voice_engine.talk("Modos: random, daily y salir")
        
        while self.is_active:
            command = self.speech_recognizer.listen_from_microphone()
            
            if command:
                self.handle_command(command)
            else:
                self.voice_engine.talk("El modo eleguido no ha sido encontrado")
    
    def exit(self, command):
        self.voice_engine.talk("saliendo del modo adivinar")
        self.is_active = False
        
    def handle_command(self, command):
        handler = self.command_handlers.get(command)
        if handler:
            handler(command)
        else:
            self.voice_engine.talk("Comando no reconocido")
    
    def start_game(self, mode):
        try:
            self.voice_engine.talk("Modo adivinanza activado. Cargando la palabra.")
            result = modeGameWord(mode)
            self.word = result['data']['word']
            self.attempts = 0

            self.voice_engine.talk(f"La palabra tiene {len(self.word)} letras. ¡Comienza!")
            self._game_loop()
            
        except Exception as e:
            print(f"Error en el juego: {e}")
            self.voice_engine.talk("Hubo un error al iniciar el juego")
    
    def _game_loop(self):
        while self.attempts < self.max_attempts:
            command = self.speech_recognizer.listen_from_microphone()
            
            if command == 'salir':
                self.voice_engine.talk('Saliendo del modo adivinanza')
                return
            elif command == 'pista':
                self._give_hint()
                continue
            
            self.attempts += 1
            
            if self._check_guess(command):
                return
                
        self._handle_game_over()
    
    def _check_guess(self, guess):
        if guess == self.word:
            self.voice_engine.talk(f'¡Correcto! Adivinaste en {self.attempts} intentos!')
            return True
        else:
            remaining = self.max_attempts - self.attempts
            self.voice_engine.talk(f'Incorrecto. Te quedan {remaining} intentos.')
            self._give_feedback(guess)
            return False
    
    def _give_hint(self):
        hint_length = min(self.attempts + 1, len(self.word))
        hint = self.word[:hint_length]
        self.voice_engine.talk(f"Pista: la palabra empieza con {hint}")
    
    def _give_feedback(self, attempt):
        try:
            if len(attempt) != len(self.word):
                self.voice_engine.talk(f"La palabra tiene {len(self.word)} letras, no {len(attempt)}")
            else:
                correct_letters = sum(1 for a, b in zip(attempt, self.word) if a == b)
                self.voice_engine.talk(f"Tienes {correct_letters} letras correctas en la posición adecuada")
        except Exception as e:
            self.voice_engine.talk('Por favor diga algo')
    
    def _handle_game_over(self):
        self.voice_engine.talk(f'Game over. La palabra era: {self.word}')
        print(f"🔍 La palabra era: {self.word}")

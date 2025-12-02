import os
import re 


HOME = os.path.expanduser("~")

class WritingVoice:
    def __init__(self, voice_engine, speech_recognizer):
        self.voice_engine = voice_engine
        self.speech_recognizer = speech_recognizer
        self.is_active = True
        
        self._handle_options()
        
    def _handle_options(self):
        self.command_handlers = {
            'personalizado': self._get_custom_filename,
            'automático': self._generate_auto_filename,
            'salir': self.exit
        }
        
    def select_name(self):
        self.voice_engine.talk("Se ha acticado el modo de escribir")
        self.voice_engine.talk("Por favor eliga si quiere un nombre personalizado o automatico")
        
        while self.is_active:
            command = self.speech_recognizer.listen_from_microphone()
            
            if command:
                self.handle_command(command)
            else:
                self.voice_engine.talk("El modo eleguido no ha sido encontrado")
    
    def handle_command(self, command):
        handler = self.command_handlers.get(command)
        if handler:
            handler()
        else:
            self.voice_engine.talk("Comando no reconocido")
    
    def _get_custom_filename(self):
        """Obtiene un nombre personalizado del usuario"""
        self.voice_engine.talk("Por favor, di el nombre del archivo")
        file_name = self.speech_recognizer.listen_from_microphone()
        
        if not file_name or file_name.strip() == '':
            self.voice_engine.talk("No escuché el nombre. Intentemos de nuevo.")
            return self._get_custom_filename()
        
        return self._clean_filename(file_name)
    
    def _generate_auto_filename(self):
        """Genera un nombre automático basado en fecha/hora"""
        from datetime import datetime
        
        now = datetime.now()
        file_name = f"nota_{now.strftime('%Y%m%d_%H%M%S')}.txt"
        
        self.voice_engine.talk(f"Usando nombre automático: {file_name}")
        self._start_writing(file_name)

    def _clean_filename(self, filename):
        filename = filename.strip().lower()
        
        filename = re.sub(r'\s+', '_', filename)
        
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        
        if len(filename) > 50:
            filename = filename[:50]
        
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        self._start_writing(filename)
    
    def _start_writing(self, file_name):
        """Inicia el proceso de escritura en el archivo"""
        file_path = f'{HOME}/Documents/{file_name}'
        
        mode = 'a' if os.path.exists(file_path) else 'w'
        
        self.voice_engine.talk(f"Escribiendo en {file_name}. Di 'salir' para terminar.")
        
        with open(file_path, mode, encoding='utf-8') as file:
            if mode == 'w':
                file.write("=== Inicio de notas ===\n\n")
            
            while True:
                try:
                    command = self.speech_recognizer.listen_from_microphone()
                    
                    if command.lower() in ['salir', 'terminar', 'fin']:
                        self.voice_engine.talk("Guardando archivo y saliendo")
                        file.write("\n=== Fin de notas ===\n")
                        break
                    
                    file.write(f"{command}\n")

                except Exception as e:
                    print(f"Error: {e}")
                    continue
                
    def exit(self):
        self.voice_engine.talk("saliendo del modo Escritura")
        self.is_active = False
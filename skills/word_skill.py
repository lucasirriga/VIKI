from .base_skill import BaseSkill
import os
import threading

class WordSkill(BaseSkill):
    def name(self):
        return "Abrir Microsoft Word"

    def match_phrases(self):
        return ["abrir word", "iniciar word", "janela do word", "word por favor"]

    def execute(self, text):
        # Usamos uma thread para os.system(start winword) não travar o loop de áudio enquanto o word estiver aberto
        def open_app():
            os.system("start winword")
            
        threading.Thread(target=open_app, daemon=True).start()
        
        # A interface devolve a fiação pura pro Main!
        return ("Abrindo Microsoft Word", "Vou abrir o Microsoft Word para você.")

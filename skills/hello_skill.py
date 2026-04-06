from .base_skill import BaseSkill

class HelloSkill(BaseSkill):
    def name(self):
        return "Saudação Matinal Básica"

    def match_phrases(self):
        # Mapeando todas as interações simples
        return ["olá", "oi", "ola", "tá me ouvindo", "ta me ouvindo", "teste", "acorde"]

    def execute(self, text):
        # Apenas código nativo, e envia os DADOS puros para o main gerir as fiações lógicas do windows e pipers.
        return ("Olá! Como posso ajudar?", "Olá! Sou a VIKI, como posso ajudar?")

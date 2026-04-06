class BaseSkill:
    def name(self):
        """Título interno ou visual da Skill"""
        return "Unknown"

    def match_phrases(self):
        """Lista de frases chave que dão trigger na skill (Ex: ['abrir word', 'iniciar word'])"""
        return []

    def execute(self, text):
        """
        Executa a instrução pura e devolve a tupla para o controle da interface de Roteamento principal:
        Retorno: (Mensagem_na_Tela_Toast, Mensagem_na_Fala_Voz)
        Exemplo: return ("Abrindo Microsoft Word", "Vou abrir o Microsoft Word para você")
        """
        return (None, None)

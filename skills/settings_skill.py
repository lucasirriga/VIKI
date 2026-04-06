import threading
from .base_skill import BaseSkill


class SettingsSkill(BaseSkill):
    def name(self):
        return "Abrir Configurações"

    def match_phrases(self):
        return [
            "configurações",
            "configuracoes",
            "abrir configurações",
            "abrir configuracoes",
            "ajustes",
            "settings",
        ]

    def execute(self, text):
        try:
            from settings_ui import open_settings_window
            threading.Thread(target=open_settings_window, daemon=True).start()
        except ImportError:
            return ("Tkinter indisponível", "Interface gráfica não disponível neste ambiente.")
        return ("Abrindo configurações", "Abrindo o painel de configurações.")

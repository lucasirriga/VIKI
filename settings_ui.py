import threading
import config_manager


def open_settings_window():
    """Abre a janela de configurações em uma thread daemon. Não bloqueia o loop de áudio."""
    t = threading.Thread(target=_run_settings_window, daemon=True)
    t.start()


def _run_settings_window():
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox
    except ImportError:
        print("[VIKI-Config] tkinter não está disponível neste ambiente.")
        return

    cfg = config_manager.load_config()

    root = tk.Tk()
    root.title("VIKI — Configurações")
    root.resizable(False, False)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    vars_ = {}  # chave -> tk.StringVar ou tk.Text

    def make_tab(label):
        frame = ttk.Frame(notebook, padding=12)
        notebook.add(frame, text=label)
        return frame

    def add_field(frame, row, label_text, key, width=45):
        ttk.Label(frame, text=label_text).grid(row=row, column=0, sticky="w", pady=4)
        var = tk.StringVar(value=str(cfg[key]))
        vars_[key] = var
        entry = ttk.Entry(frame, textvariable=var, width=width)
        entry.grid(row=row, column=1, sticky="ew", padx=(10, 0), pady=4)

    # ---- Aba Áudio / STT ----
    tab_stt = make_tab("Áudio / STT")
    add_field(tab_stt, 0, "Busca de microfone:",          "mic_search_string")
    add_field(tab_stt, 1, "Timeout STT (s):",             "stt_timeout")
    add_field(tab_stt, 2, "Tempo limite de frase (s):",   "stt_phrase_time_limit")
    add_field(tab_stt, 3, "Idioma STT:",                  "stt_language")
    add_field(tab_stt, 4, "Limiar de energia:",           "energy_threshold")
    add_field(tab_stt, 5, "Calibração de ruído (s):",     "ambient_calibration_duration")
    add_field(tab_stt, 6, "Pausa entre ciclos (s):",      "loop_sleep")

    # ---- Aba LLM ----
    tab_llm = make_tab("LLM")
    add_field(tab_llm, 0, "URL da API Ollama:",  "ollama_url",     width=55)
    add_field(tab_llm, 1, "Modelo:",             "llm_model")
    add_field(tab_llm, 2, "Máx. tokens:",        "llm_max_tokens")
    add_field(tab_llm, 3, "Temperatura:",        "llm_temperature")
    add_field(tab_llm, 4, "Timeout (s):",        "llm_timeout")
    ttk.Label(tab_llm, text="System Prompt:").grid(row=5, column=0, sticky="nw", pady=4)
    sys_text = tk.Text(tab_llm, width=55, height=6, wrap="word")
    sys_text.insert("1.0", cfg["llm_system_prompt"])
    sys_text.grid(row=5, column=1, sticky="ew", padx=(10, 0), pady=4)
    vars_["llm_system_prompt"] = sys_text  # widget Text, não StringVar

    # ---- Aba TTS ----
    tab_tts = make_tab("TTS")
    add_field(tab_tts, 0, "Executável Piper:",   "piper_exe",        width=55)
    add_field(tab_tts, 1, "URL modelo de voz:",  "voice_model_url",  width=55)
    add_field(tab_tts, 2, "URL config de voz:",  "voice_config_url", width=55)

    # ---- Tipos numéricos para validação ----
    _INT_KEYS   = {"stt_timeout", "stt_phrase_time_limit", "energy_threshold",
                   "ambient_calibration_duration", "llm_max_tokens", "llm_timeout"}
    _FLOAT_KEYS = {"llm_temperature", "loop_sleep"}

    def on_save():
        new_cfg = {}
        for key, widget in vars_.items():
            if isinstance(widget, tk.Text):
                new_cfg[key] = widget.get("1.0", "end-1c")
            else:
                raw = widget.get().strip()
                try:
                    if key in _INT_KEYS:
                        new_cfg[key] = int(raw)
                    elif key in _FLOAT_KEYS:
                        new_cfg[key] = float(raw)
                    else:
                        new_cfg[key] = raw
                except ValueError:
                    messagebox.showerror(
                        "Valor inválido",
                        f"O campo '{key}' contém um valor inválido: '{raw}'\n"
                        f"Corrija antes de salvar."
                    )
                    return
        config_manager.save_config(new_cfg)
        print("[VIKI-Config] Configurações salvas com sucesso.")
        root.destroy()

    ttk.Button(root, text="Salvar e Fechar", command=on_save).pack(pady=(0, 12))
    root.mainloop()


if __name__ == "__main__":
    open_settings_window()

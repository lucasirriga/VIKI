import json
import os
import copy

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(_SCRIPT_DIR, "config.json")

DEFAULTS = {
    # --- STT / Áudio ---
    "mic_search_string": "QCY",
    "stt_timeout": 8,
    "stt_phrase_time_limit": 10,
    "stt_language": "pt-BR",
    "energy_threshold": 300,
    "ambient_calibration_duration": 2,
    "loop_sleep": 0.5,

    # --- LLM ---
    "ollama_url": "http://localhost:11434/api/generate",
    "llm_model": "gemma3:1b",
    "llm_max_tokens": 70,
    "llm_temperature": 0.6,
    "llm_timeout": 20,
    "llm_system_prompt": (
        "Você é a VIKI, uma assistente virtual de voz. Seja objetiva, seca e carismática.\n"
        "Jamais envie formatações de texto como asteriscos, negritos ou listas, pois sua resposta será sintetizada em uma caixa de ÁUDIO.\n"
        "Responda sempre em no MÁXIMO 2 frases puras e muito diretas."
    ),

    # --- TTS ---
    "piper_exe": os.path.join(_SCRIPT_DIR, "venv", "Scripts", "piper.exe"),
    "voice_model_url": (
        "https://huggingface.co/rhasspy/piper-voices/resolve/main/"
        "pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx?download=true"
    ),
    "voice_config_url": (
        "https://huggingface.co/rhasspy/piper-voices/resolve/main/"
        "pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx.json?download=true"
    ),
}


def load_config() -> dict:
    cfg = copy.deepcopy(DEFAULTS)
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            overrides = json.load(f)
        cfg.update(overrides)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return cfg


def save_config(cfg: dict) -> None:
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


def get(key: str):
    return load_config()[key]

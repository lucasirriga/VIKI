import requests
import config_manager

def ask_gemma(prompt):
    cfg = config_manager.load_config()

    payload = {
        "model": cfg["llm_model"],
        "prompt": f"{cfg['llm_system_prompt']}\n\n[USUÁRIO]: {prompt}\n[VIKI]:",
        "stream": False,
        "options": {
            "num_predict": cfg["llm_max_tokens"],  # Impede que ela fale textos massivos longos pro motor TTS travar
            "temperature": cfg["llm_temperature"]
        }
    }

    try:
        print("[VIKI] LLM Local (Ollama) foi Acionado. Gerando Inferência...")
        response = requests.post(cfg["ollama_url"], json=payload, timeout=cfg["llm_timeout"])  # Pode demorar alguns segundos rodando em CPU/Máquina
        if response.status_code == 200:
            return response.json().get("response", "").strip()
        else:
            print(f"[ERRO LLM] Código: {response.status_code}")
            return "Desculpe, meu nó de intelecto falhou internamente."
    except Exception as e:
        print(f"[ERRO LLM FATAL] {e}")
        return "Minha rede neural está offline ou o Ollama não respondeu."

import requests

def ask_gemma(prompt):
    url = "http://localhost:11434/api/generate"
    
    # Behavior forçado para ela ser rápida e objetiva no áudio
    sys_prompt = """Você é a VIKI, uma assistente virtual de voz. Seja objetiva, seca e carismática. 
Jamais envie formatações de texto como asteriscos, negritos ou listas, pois sua resposta será sintetizada em uma caixa de ÁUDIO. 
Responda sempre em no MÁXIMO 2 frases puras e muito diretas."""

    payload = {
        "model": "gemma2:2b",
        "prompt": f"{sys_prompt}\n\n[USUÁRIO]: {prompt}\n[VIKI]:",
        "stream": False,
        "options": {
            "num_predict": 70, # Impede que ela fale textos massivos longos pro motor TTS travar
            "temperature": 0.6
        }
    }
    
    try:
        print("[VIKI] LLM Local (Ollama) foi Acionado. Gerando Inferência...")
        response = requests.post(url, json=payload, timeout=20)   # Pode demorar alguns segundos rodando em CPU/Máquina
        if response.status_code == 200:
            return response.json().get("response", "").strip()
        else:
            print(f"[ERRO LLM] Código: {response.status_code}")
            return "Desculpe, meu nó de intelecto falhou internamente."
    except Exception as e:
        print(f"[ERRO LLM FATAL] {e}")
        return "Minha rede neural está offline ou o Ollama não respondeu."

import time
import speech_recognition as sr
from win11toast import toast
from tts import speak
import os
import importlib
import inspect
from skills.base_skill import BaseSkill
from llm import ask_gemma

def carregar_skills():
    """Varre a pasta skills dinamicamente e carrega na memória RAM da Viki"""
    carregadas = []
    print("[VIKI] Carregando conexões sinápticas (Skills)...")
    skills_dir = os.path.join(os.path.dirname(__file__), "skills")
    
    for filename in os.listdir(skills_dir):
        if filename.endswith(".py") and not filename.startswith("__") and filename != "base_skill.py":
            module_name = f"skills.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                # Enrola todo mundo que herda da interface padrão
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, BaseSkill) and obj is not BaseSkill:
                        skill_instance = obj()
                        carregadas.append(skill_instance)
                        print(f"       + Conectada: {skill_instance.name()}")
            except Exception as e:
                print(f"       [ERRO] Falha ao injetar skill do arquivo {filename}: {e}")
                
    return carregadas

def listen_and_transcribe(recognizer, source):
    print("[VIKI] Ouvindo...")
    try:
        # Aumentamos o timeout levemente, mas agora ela escuta direto sem ajustar ruidos a todo momento
        audio = recognizer.listen(source, timeout=8, phrase_time_limit=10)
        print("[VIKI] Processando sua fala (STT)...")
        text = recognizer.recognize_google(audio, language="pt-BR")
        print(f"[VOCE] {text}")
        return text.lower()
    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        print("[VIKI] (Não entendi o que foi dito)")
        return ""
    except sr.RequestError as e:
        print(f"[VIKI] Erro no serviço de STT: {e}")
        return ""
    except Exception as e:
        print(f"[VIKI] Erro inesperado: {e}")
        return ""

def main():
    print("Iniciando a VIKI Core Loop...")
    toast("VIKI Iniciada", "Assistente de voz conectada e operante.")
    
    # Debug de microfones e seleção inteligente
    qcy_index = None
    try:
        mics = sr.Microphone.list_microphone_names()
        for idx, m in enumerate(mics):
            if "QCY" in m and qcy_index is None:
                qcy_index = idx # Salva o primeiro QCY que achar
                
        if qcy_index is not None:
             print(f"\n[VIKI] Sucesso: Encontrei o seu fone QCY no índice {qcy_index}! Prendendo áudio nele.")
        else:
             print("\n[VIKI] ALERTA: Não consegui achar 'QCY' na lista, usando o padrão do Windows.")
             
    except Exception as e:
         print(f"[DEBUG] Erro lendo mics: {e}")
         
    recognizer = sr.Recognizer()
    # Desligar o ajuste automático constante
    recognizer.dynamic_energy_threshold = False 
    
    # Microfone fica aberto continuadamente e travado no QCY
    with sr.Microphone(device_index=qcy_index) as source:
        print("\n[VIKI] Calibrando microfone (fique em silêncio por 2 segundos)...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        # Trava um limite manualmente máximo sensível caso o ajuste erre pra cima
        if recognizer.energy_threshold > 1000:
            print("[DEBUG] O Windows reportou muito ruído. Forçando alta sensibilidade (300).")
            recognizer.energy_threshold = 300
            
        print(f"[VIKI] Calibrada! Limiar de som (Threshold) fixado em: {recognizer.energy_threshold:.2f}")
        print("[VIKI] Pronta para ouvir.")
        
        skills_ativas = carregar_skills()
        
        while True:
            text = listen_and_transcribe(recognizer, source)
            
            if text:
                # O [VOCE] imprime la no listn_and... entao é só processar a lógica
                encontrada = False
                
                # Match Loop (Complexidade O(n)) - A Viki tenta ver em seu catálogo se tem a Skill exata (Gatilho Fixo)
                for skill in skills_ativas:
                    # Verifica se alguma frase do Match Pattern dessa skill foi ouvida
                    if any(phrase in text for phrase in skill.match_phrases()):
                        print(f"[VIKI] Roteador Local -> Gatilho cravado na Skill: {skill.name()}")
                        
                        resultado = skill.execute(text)
                        
                        # Processamento puro da view
                        if resultado and len(resultado) == 2:
                            texto_toast, texto_speak = resultado
                            if texto_toast:
                                toast("VIKI", texto_toast)
                            if texto_speak:
                                speak(texto_speak)
                                
                        encontrada = True
                        break # Para no primeiro que se prontificar a responder
                
                # Fallback Loop (Gatilho Complexo) - Joga no LLM
                if not encontrada:
                    print(f"[VIKI] Intenção '{text}' enviada para a API Local Gemma 3.")
                    toast("VIKI (Cérebro Neural)", "🧠 Pensando...")
                    
                    resposta_inteligente = ask_gemma(text)
                    print(f"[VIKI/Gemma] {resposta_inteligente}")
                    
                    toast("VIKI", resposta_inteligente)
                    speak(resposta_inteligente)
                
        time.sleep(0.5)

if __name__ == "__main__":
    main()

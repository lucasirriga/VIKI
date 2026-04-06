import os
import urllib.request
import wave
import pyaudio
import sys
import config_manager

MODEL_FILE = os.path.join(os.path.dirname(__file__), "viki_voice.onnx")
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "viki_voice.onnx.json")

def download_voice_if_not_exists():
    if not os.path.exists(MODEL_FILE):
        cfg = config_manager.load_config()
        print("\n[VIKI-TTS] Fazendo download da nova matriz de voz offline (Faber pt-BR).")
        print("[VIKI-TTS] Isso só acontece na primeira vez e pesa ~50MB. Aguarde um instante...")
        urllib.request.urlretrieve(cfg["voice_model_url"], MODEL_FILE)
        urllib.request.urlretrieve(cfg["voice_config_url"], CONFIG_FILE)
        print("[VIKI-TTS] Instalação de voz 100% concluída!\n")

def speak(text):
    download_voice_if_not_exists()
    try:
        import subprocess
        wav_path = "viki_cache.wav"
        piper_exe = config_manager.get("piper_exe")
        text_file = os.path.join(os.path.dirname(__file__), "temp_text.txt")

        # UTF-8 com Marca de Ordem de Byte (BOM) é nativamente reconhecido por binários C++ no Windows
        with open(text_file, "w", encoding="utf-8-sig") as f:
            f.write(text)

        # Rodamos o Piper dizendo pra ele LER o arquivo diretamente por dentro
        # (assim não passamos pela codepage bugada do terminal)
        cmd = f'"{piper_exe}" -m "{MODEL_FILE}" -c "{CONFIG_FILE}" -f "{wav_path}" -i "{text_file}"'

        result = subprocess.run(cmd, shell=True, capture_output=True)

        if result.returncode != 0:
            print(f"[VIKI-TTS] O Motor Piper falhou: {result.stderr.decode('utf-8', errors='ignore')}")
            return

        _play_wav(wav_path)

    except Exception as e:
        print(f"[VIKI-TTS] Erro fatal no motor de fala: {e}")

def _play_wav(path):
    wf = wave.open(path, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(1024)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(1024)
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    text = "Sistemas offline funcionando perfeitamente. Olá mestre."
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    speak(text)

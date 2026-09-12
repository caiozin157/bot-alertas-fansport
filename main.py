import requests
import time

TELEGRAM_BOT_TOKEN = "8682771541:AAHB_FC-nTSi4HXWhNB_Hpv0rGUs5qbFvpc"
TELEGRAM_CHAT_ID = "6395967105"
API_FOOTBALL_KEY = "00ac37fde5a188f6dd1c6d780e1d87a3"

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

def obter_jogos_ao_vivo():
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {"x-apisports-key": API_FOOTBALL_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("response", [])
    return []

def analisar_jogo(jogo):
    # Lógica de análise baseada em dados estatísticos
    tempo = jogo['fixture']['status']['elapsed']
    if not tempo or tempo < 15:
        return None

    equipas = f"{jogo['teams']['home']['name']} vs {jogo['teams']['away']['name']}"

    # Exemplo de regra automática de alerta
    return f"🔥 Oportunidade detetada no jogo {equipas} ({tempo}')!"

def executar_bot():
    print("A verificar jogos ao vivo...")
    jogos = obter_jogos_ao_vivo()
    for jogo in jogos:
        alerta = analisar_jogo(jogo)
        if alerta:
            enviar_telegram(alerta)

if __name__ == "__main__":
    while True:
        try:
            executar_bot()
        except Exception as e:
            print(f"Erro: {e}")
        time.sleep(300)


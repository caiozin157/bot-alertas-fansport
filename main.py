import requests
import time
import anthropic
import os

TELEGRAM_BOT_TOKEN = "8682771541:AAHB_FC-nTSi4HXWhNB_Hpv0rGUs5qbFvpc"
TELEGRAM_CHAT_ID = "6395967105"
API_FOOTBALL_KEY = "00ac37fde5a188f6dd1c6d780e1d87a3"
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

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

def analisar_jogo_com_claude(dados_jogo):
    prompt = f"""
    Analisa os seguintes dados em tempo real para oportunidades de apostas (Fansport):
    {dados_jogo}

    Se houver um padrão claro (alta pressão de cantos, remates à baliza, golo iminente), gera um alerta curto em português.
    Se não for relevante, responde apenas 'SEM_ALERTA'.
    """
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def executar_bot():
    print("A verificar jogos...")
    jogos = obter_jogos_ao_vivo()
    for jogo in jogos:
        equipas = f"{jogo['teams']['home']['name']} vs {jogo['teams']['away']['name']}"
        tempo = jogo['fixture']['status']['elapsed']
        if tempo and tempo > 15:
            analise = analisar_jogo_com_claude(jogo)
            if analise != "SEM_ALERTA":
                mensagem = f"🚨 *ALERTA DE JOGO*\n\n⚽ *{equipas}* ({tempo}')\n\n{analise}"
                enviar_telegram(mensagem)

if __name__ == "__main__":
    while True:
        try:
            executar_bot()
        except Exception as e:
            print(f"Erro: {e}")
        time.sleep(300)

import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

url = os.getenv("N8N_WEBHOOK_URL")
dados = {
    "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    "conteudo": "Teste de conexão do sistema, Senhor.",
    "dispositivo": "Terminal Stark",
    "ip": "127.0.0.1"
}

response = requests.post(url, json=dados)
print(f"Status: {response.status_code}")
print(f"Resposta: {response.text}")
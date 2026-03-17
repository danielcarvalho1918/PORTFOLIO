import requests

# COLE AQUI a Test URL que você copiou do n8n
url = "http://localhost:5678/webhook-test/captura-leads-rocket"

dados = {
    "nome": "Daniel Researcher",
    "email": "daniel@exemplo.com",
    "empresa": "UECE"
}

response = requests.post(url, json=dados)

print(f"Status Code: {response.status_code}")
print(f"Resposta do n8n: {response.text}")
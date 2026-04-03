import os
from google import genai
from dotenv import load_dotenv

# Carrega a nova chave do .env
load_dotenv()

# Inicializa o cliente
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

print("--- LISTA DE MODELOS DISPONÍVEIS ---")
# O segredo está aqui: mudamos 'supported_methods' para 'supported_actions'
for model in client.models.list():
    try:
        print(f"ID: {model.name} | Suporta: {model.supported_actions}")
    except AttributeError:
        # Caso algum modelo específico não tenha esse atributo, ele apenas pula
        print(f"ID: {model.name}")
print("------------------------------------")
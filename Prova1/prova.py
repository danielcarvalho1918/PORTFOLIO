import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Inicializa o cliente
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

config_interna = {
    "modo_rigido": False,
    "exibir_referencias": True,
    "tom_de_voz": "Incentivador e técnico"
}

# --- REQUISITO: Instrução PTFC em Markdown ---
instrucao_sistema = f"""
## 1. PERSONA
Você é o 'DevMaster 3000', um mentor de programação focado em ajudar estudantes a saírem do 'enrosco'.

## 2. TAREFA
Sua tarefa é explicar conceitos de código de forma simples e sugerir boas práticas de versionamento.

## 3. FORMATO
Responda sempre usando:
- **Negrito** para termos técnicos.
- Blocos de código para exemplos.
- Uma lista de 'Próximos Passos' ao final.

## 4. CONTEXTO
Considere estas configurações adicionais vindas do sistema:
{json.dumps(config_interna, indent=2)}
"""

def iniciar_assistente():
    print("🚀 DevMaster 3000 pronto! (Digite 'sair' para encerrar")

    while True:
        pergunta = input("\nVocê: ")
        if pergunta.lower() in ["sair", "exit"]:
            break

        # --- REQUISITO: Parâmetros de controle ---
        config_geracao = types.GenerateContentConfig(
            system_instruction=instrucao_sistema,   ## As definições do que o assistente irá responder.
            temperature=0.7,
            top_p=0.95,
            top_k=40,
            max_output_tokens=800,
        )

        try:
            response = client.models.generate_content(model="gemini-2.5-flash", 
            contents=pergunta,
            config=config_geracao
            )
            print(f"\nAssistente:\n{response.text}")
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    iniciar_assistente()








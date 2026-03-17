import sys
import os # Para manipular variáveis de ambiente (como chaves de API)
import asyncio # # Para lidar com funções assíncronas (que rodam em segundo plano)
import gradio as gr # Biblioteca para criar a interface visual do chat rapidamente
from google import genai  # SDK oficial do Google para usar o Gemini
from dotenv import load_dotenv  # Carrega as configurações do arquivo .env
from google.genai import types  # Importa tipos de dados específicos para configurar o modelo
from rag_utils import RAGEngine  # Um módulo local (provavelmente criado pelo seu professor) para lidar com PDFs
from mcp.client.stdio import stdio_client  # Cliente para o Model Context Protocol (MCP)
from mcp import ClientSession, StdioServerParameters  # Sessão e parâmetros para o MCP


load_dotenv() # Ativa a leitura do arquivo .env

api_key = os.environ.get("GOOGLE_API_KEY")

client = genai.Client() # Inicializa o cliente que vai conversar com os servidores do Google


# (As linhas comentadas com # abaixo serviam para listar modelos e preparar os PDFs 
# diretamente no script, mas parece que agora isso foi movido para o servidor MCP)

# Configura como o script vai "chamar" o servidor de contexto (um processo separado)
server_params = StdioServerParameters(
    command=sys.executable, # Isso força o Jarvis a usar o MESMO Python que ele está usando
    args=["mcp_server.py"],
    env=os.environ
)

# Abre o arquivo 'jarvis.md' que contém a "personalidade" ou instruções do robô
with open("jarvis.md", "r", encoding="utf-8") as f:
    system_instructions = f.read()


# Cria a sessão de chat configurando o modelo Gemini
chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=system_instructions, # O que o Jarvis deve ou não fazer
        temperature=1.7, # Nível de criatividade (1.7 é bem alto, ele será bem expressivo)
        top_p=0.9, # Técnica de amostragem para escolher palavras prováveis
        top_k=50,  # Limita o vocabulário às 50 palavras mais prováveis
        max_output_tokens=2048  # Tamanho máximo da resposta
    )
)

# Função que "pergunta" ao servidor MCP se existem documentos sobre o que o usuário quer saber
async def consultar_servidor_mcp(pergunta: str):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize() # Inicia a conexão com o servidor de documentos
            # Chama a ferramenta específica de consulta
            result = await session.call_tool(
                "consultar_documentacao",
                arguments={"pergunta": pergunta}
            )
            # Se encontrar texto nos documentos, retorna; senão, avisa que não achou
            if result.content and len(result.content) > 0:
                return result.content[0].text
            return "Nenhuma informação encontrada."

# Função principal que gera a resposta final
async def generate_response(user_message, chat_history):
    try:
        # 1. Primeiro, ele busca nos PDFs (via MCP) algo sobre o assunto
        contexto_encontrado = await consultar_servidor_mcp(user_message)

        # 2. Ele monta um "prompt" turbinado com a pergunta + o texto dos PDFs
        mensagem_com_contexto = f""""
        Mensagem do usuário: {user_message}
        Contexto relevante: {contexto_encontrado}
        Responda à mensagem do usuário utilizando o contexto encontrado...
        """

        # 3. Envia tudo para o Gemini e recebe a resposta final
        response = chat.send_message(mensagem_com_contexto)
        return response.text
    except Exception as e:
        return f"Ocorreu um erro: {str(e)}"


# Cria a interface gráfica (janela de chat) que você vê no navegador
demo = gr.ChatInterface(
    fn=generate_response,
    title="Jarvis - Assistente Virtual",
    description="Converse com o Jarvis diretamente pelo navegador."
)

if __name__ == "__main__":
    demo.launch() # Roda o app


















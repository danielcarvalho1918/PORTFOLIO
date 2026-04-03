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
        temperature=0.1, # Nível de criatividade (1.7 é bem alto, ele será bem expressivo)
        top_p=0.95, # Técnica de amostragem para escolher palavras prováveis
        top_k=40,  # Limita o vocabulário às 50 palavras mais prováveis
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


import gradio as gr

# --- 1. CONFIGURAÇÃO ESTÉTICA (CSS DE ALTA INTENSIDADE) ---
custom_css = """
.titulo-container {
    text-align: center;
    padding: 20px;
    background: rgba(0, 255, 255, 0.05);
    border-radius: 10px;
    border: 1px solid #00FFFF;
    margin-bottom: 20px;
}
.titulo-neon {
    color: #00FFFF !important;
    text-shadow: 0 0 15px #00FFFF, 0 0 30px #00FFFF !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 2.5em !important;
    margin: 0 !important;
}
.subtitulo-neon {
    color: #00FFFF !important;
    opacity: 0.8;
    font-family: 'Orbitron', sans-serif !important;
}
"""

theme = gr.themes.Soft(
    primary_hue="cyan",
    neutral_hue="slate",
).set(
    body_background_fill="#050505",
    block_background_fill="#0a0a0a",
    block_border_width="1px",
    border_color_primary="#00FFFF",
)

# --- 2. CONSTRUÇÃO DA INTERFACE ---
with gr.Blocks(css=custom_css, theme=theme, title="Jarvis Concurseiro") as demo:
    # Título usando HTML puro para garantir que o CSS seja aplicado
    gr.HTML(
        """
        <div class="titulo-container">
            <h1 class="titulo-neon">🤖 JARVIS CONCURSEIRO</h1>
            <p class="subtitulo-neon">Sistemas de Apoio Estratégico - Protocolo de Aprovação Daniel Carvalho</p>
        </div>
        """
    )
    
    # Removido o argumento 'type' para evitar o erro de inicialização
    chatbot = gr.Chatbot(show_label=False, height=500)
    
    with gr.Row():
        msg = gr.Textbox(
            placeholder="Digite seu comando tático aqui, Senhor...",
            show_label=False,
            scale=9
        )
        submit = gr.Button("ENVIAR", variant="primary", scale=1)

    # --- 3. LÓGICA DE DADOS (FORMATO DE DICIONÁRIO EXIGIDO PELO SEU LOG) ---
    async def respond(message, chat_history):
        # Chama sua função original de resposta
        bot_message = await generate_response(message, chat_history)
        
        # O LOG DE ERRO EXIGE ESTE FORMATO: dicionário com 'role' e 'content'
        # Mesmo que o chatbot não tenha type="messages", o processamento interno da sua versão pede isso
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": bot_message})
        
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    submit.click(respond, [msg, chatbot], [msg, chatbot])

# --- 4. LANÇAMENTO ---
if __name__ == "__main__":
    demo.launch(share=False)

# Cria a interface gráfica (janela de chat) que você vê no navegador
#demo = gr.ChatInterface(
#    fn=generate_response,
#    title="Jarvis Concurseiro - Assistente Virtual",
#    description="Converse com o Jarvis diretamente pelo navegador."
#)

#if __name__ == "__main__":
#    demo.launch() # Roda o app














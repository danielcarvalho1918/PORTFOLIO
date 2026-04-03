import os  # Para ler variáveis de ambiente (como chaves de API)
import sys  # Para enviar mensagens de log para o sistema (standard error)
from dotenv import load_dotenv  # Carrega as configurações do arquivo .env
from rag_utils import RAGEngine  # Importa a ferramenta que "lê" e organiza os PDFs
from mcp.server.fastmcp import FastMCP  # Biblioteca que cria o servidor de comunicação (MCP)

load_dotenv() # Ativa o carregamento da API Key do arquivo .env

# Cria uma instância do servidor MCP chamada "Jarbas" na versão 0.1
mcp = FastMCP("Servidor de MCP do Jarvis", "0.1")

# Lista de caminhos para os arquivos PDF que o Jarbas deve "estudar"
arquivos_pdf = [
    "Inteligencia_Artificial_Aprofundado.pdf",
    "Machine_Learning_Aprofundado.pdf"
]

# Mensagem enviada para o console avisando que o motor de busca está iniciando
print(" Carregando RAG Engine", file=sys.stderr)

# Inicializa o motor de RAG passando a lista de PDFs acima. 
# Aqui ele transforma os PDFs em "vetores" (números) para busca rápida.
rag_engine = RAGEngine(pdf_paths=arquivos_pdf)

# Define uma "Ferramenta" (Tool) que o Gemini poderá chamar via protocolo MCP
@mcp.tool()
def consultar_documentacao(pergunta: str) -> str:
    """
    Esta função recebe uma pergunta e usa o rag_engine para
    procurar a resposta nos PDFs carregados.
    """

    try:
        # Tenta buscar o texto relevante nos PDFs
        contexto = rag_engine.buscar_contexto(pergunta)

        # Se não achar nada útil, retorna uma mensagem padrão
        if not contexto:
            return "Desculpe, não consegui encontrar informações relevantes nos documentos."

        # Se achar, retorna o trecho do PDF para ser usado pela IA
        return contexto
    except Exception as e:
        # Caso ocorra algum erro técnico, retorna a descrição do erro
        return f"Erro ao buscar contexto: {str(e)}"
    
# Se o script for executado diretamente, inicia o servidor MCP
if __name__ == "__main__":
    mcp.run()



















































import os  # Para ler variáveis de ambiente (como chaves de API)
import sys  # Para enviar mensagens de log para o sistema (standard error)
from dotenv import load_dotenv  # Carrega as configurações do arquivo .env
from rag_utils import RAGEngine  # Importa a ferramenta que "lê" e organiza os PDFs
from mcp.server.fastmcp import FastMCP  # Biblioteca que cria o servidor de comunicação (MCP)

load_dotenv() # Ativa o carregamento da API Key do arquivo .env

# Cria uma instância do servidor MCP chamada "Jarbas" na versão 0.1
mcp = FastMCP("Servidor de MCP do Jarvis", "0.1")

arquivos_pdf = ["pdfs/curso-247076-aula-01-profs-paolla-ramos-e-raphael-lacerda-f351-completo.pdf"]

# Lista de caminhos para os arquivos PDF que o Jarbas deve "estudar"
"""arquivos_pdf = [
    "pdfs/algoritmos-de-ordenacao-e-complexidade-big-o-notation-pptx.pdf",
    "pdfs/apostila - Copia.pdf",
    "pdfs/Apostila.pdf",
    "pdfs/aula-03-ataques-e-malwares.pdf",
    "pdfs/curso-228540-aula-10-c9e6-completo.pdf",
    "pdfs/curso-228540-aula-12-254f-completo.pdf",
    "pdfs/curso-236259-aula-09-86ae-completo.pdf",
    "pdfs/curso-236260-aula-04-grifado-5808.pdf",
    "pdfs/curso-236260-aula-05-b36b-completo.pdf",
    "pdfs/curso-236260-aula-05-grifado-9dc2.pdf",
    "pdfs/curso-236260-aula-06-c1ba-completo.pdf",
    "pdfs/curso-236260-aula-06-grifado-02be.pdf",
    "pdfs/curso-236260-aula-07-101d-completo.pdf",
    "pdfs/curso-236260-aula-07-grifado-3b2f.pdf",
    "pdfs/curso-236260-aula-08-b7aa-completo.pdf",
    "pdfs/curso-236260-aula-08-grifado-25dd.pdf",
    "pdfs/curso-236260-aula-11-bd94-completo.pdf",
    "pdfs/curso-236260-aula-11-grifado-1f89.pdf",
    "pdfs/curso-236260-aula-12-a45c-completo.pdf",
    "pdfs/curso-236260-aula-12-grifado-4837.pdf",
    "pdfs/curso-236260-aula-13-b2f7-completo.pdf",
    "pdfs/curso-236260-aula-13-grifado-9a11.pdf",
    "pdfs/curso-236260-aula-15-3087-completo.pdf",
    "pdfs/curso-236260-aula-15-grifado-8829.pdf",
    "pdfs/curso-247075-aula-unica-prof-evandro-28b5-completo.pdf",
    "pdfs/curso-247076-aula-00-profs-paolla-ramos-e-raphael-lacerda-ec61-completo.pdf",
    "pdfs/curso-247076-aula-01-profs-paolla-ramos-e-raphael-lacerda-f351-completo.pdf",
    "pdfs/curso-247076-aula-02-profs-paolla-ramos-e-raphael-lacerda-f5a6-completo.pdf",
    "pdfs/curso-247076-aula-03-profs-paolla-ramos-e-raphael-lacerda-e1e3-completo.pdf",
    "pdfs/curso-247076-aula-04-profs-paolla-ramos-e-raphael-lacerda-b675-completo - Copia.pdf",
    "pdfs/curso-247076-aula-05-profs-paolla-ramos-e-raphael-lacerda-415b-completo.pdf",
    "pdfs/curso-247076-aula-06-profs-paolla-ramos-e-raphael-lacerda-4440-completo.pdf",
    "pdfs/curso-247076-aula-07-profs-paolla-ramos-e-raphael-lacerda-421a-completo.pdf",
    "pdfs/curso-247076-aula-09-profs-paolla-ramos-e-raphael-lacerda-6acd-completo.pdf",
    "pdfs/curso-247076-aula-11-profs-paolla-ramos-e-raphael-lacerda-d515-completo.pdf",
    "pdfs/curso-247076-aula-12-profs-paolla-ramos-e-raphael-lacerda-5280-completo.pdf",
    "pdfs/curso-247076-aula-13-profs-paolla-ramos-e-raphael-lacerda-ec5b-completo.pdf",
    "pdfs/curso-247076-aula-15-profs-paolla-ramos-e-raphael-lacerda-cc14-completo.pdf",
    "pdfs/curso-247076-aula-16-profs-paolla-ramos-e-raphael-lacerda-ce50-completo.pdf",
    "pdfs/curso-247077-aula-00-b39e-completo.pdf",
    "pdfs/curso-247077-aula-01-1f85-completo.pdf",
    "pdfs/curso-247077-aula-02-ba82-completo.pdf",
    "pdfs/curso-247077-aula-03-98a5-completo.pdf",
    "pdfs/curso-247077-aula-04-63f9-completo.pdf",
    "pdfs/curso-247077-aula-05-f324-completo.pdf",
    "pdfs/curso-247077-aula-06-5c83-completo.pdf",
    "pdfs/curso-247077-aula-extra-cafe-completo.pdf",
    "pdfs/curso-247078-aula-00-profs-diego-carvalho-e-fernando-pedrosa-120b-completo.pdf",
    "pdfs/curso-247078-aula-01-profs-diego-carvalho-e-fernando-pedrosa-9a60-completo.pdf",
    "pdfs/curso-247078-aula-03-profs-diego-carvalho-e-fernando-pedrosa-a6da-completo.pdf",
    "pdfs/curso-247078-aula-04-profs-diego-carvalho-e-fernando-pedrosa-e1f5-completo.pdf",
    "pdfs/curso-247078-aula-05-profs-diego-carvalho-e-fernando-pedrosa-9b03-completo.pdf",
    "pdfs/curso-247078-aula-06-profs-diego-carvalho-e-fernando-pedrosa-42b1-completo.pdf",
    "pdfs/curso-247078-aula-07-profs-diego-carvalho-e-fernando-pedrosa-487f-completo.pdf",
    "pdfs/curso-247078-aula-09-profs-diego-carvalho-e-fernando-pedrosa-3078-completo.pdf",
    "pdfs/curso-247078-aula-10-profs-diego-carvalho-e-fernando-pedrosa-9354-completo.pdf",
    "pdfs/curso-247078-aula-11-profs-diego-carvalho-e-fernando-pedrosa-9aa8-completo.pdf",
    "pdfs/curso-247078-aula-12-profs-diego-carvalho-e-fernando-pedrosa-933a-completo.pdf",
    "pdfs/curso-247078-aula-13-profs-diego-carvalho-e-fernando-pedrosa-be3a-completo.pdf",
    "pdfs/curso-247078-aula-14-9c38-completo.pdf",
    "pdfs/curso-247079-aula-unica-profs-paolla-ramos-e-fernando-pedrosa-4921-completo.pdf",
    "pdfs/curso-247080-aula-00-prof-thiago-cavalcanti-826b-completo.pdf",
    "pdfs/curso-247080-aula-01-prof-thiago-cavalcanti-7622-completo.pdf",
    "pdfs/curso-247080-aula-02-prof-thiago-cavalcanti-2833-completo.pdf",
    "pdfs/curso-247080-aula-03-prof-thiago-cavalcanti-a543-completo.pdf",
    "pdfs/curso-247080-aula-04-prof-thiago-cavalcanti-3013-completo.pdf",
    "pdfs/curso-247080-aula-06-prof-thiago-cavalcanti-3539-completo.pdf",
    "pdfs/curso-247080-aula-07-prof-thiago-cavalcanti-a11a-completo.pdf",
    "pdfs/curso-247080-aula-08-prof-thiago-cavalcanti-5fc5-completo.pdf",
    "pdfs/curso-247080-aula-09-prof-thiago-cavalcanti-4cab-completo.pdf",
    "pdfs/curso-247080-aula-10-prof-thiago-cavalcanti-4df9-completo.pdf",
    "pdfs/curso-247080-aula-11-prof-thiago-cavalcanti-b57e-completo.pdf",
    "pdfs/curso-247080-aula-12-prof-thiago-cavalcanti-9340-completo.pdf",
    "pdfs/curso-247080-aula-13-prof-thiago-cavalcanti-ca50-completo.pdf",
    "pdfs/curso-247080-aula-14-profs-thiago-cavalcanti-e-raphael-lacerda-b7d9-completo.pdf",
    "pdfs/curso-247080-aula-16-d1d8-completo.pdf",
    "pdfs/curso-247136-aula-00-d2e9-completo.pdf",
    "pdfs/curso-247136-aula-01-ab07-completo.pdf",
    "pdfs/curso-247136-aula-02-dd91-completo.pdf",
    "pdfs/curso-247136-aula-03-d9b0-completo.pdf",
    "pdfs/curso-247136-aula-04-7d27-completo.pdf",
    "pdfs/curso-247136-aula-05-3328-completo.pdf",
    "pdfs/curso-247136-aula-06-8ea1-completo.pdf",
    "pdfs/curso-247136-aula-07-4ccf-completo.pdf",
    "pdfs/curso-247136-aula-08-dd4f-completo.pdf",
    "pdfs/curso-247136-aula-09-854b-completo.pdf",
    "pdfs/curso-247136-aula-10-ad8e-completo.pdf",
    "pdfs/curso-247136-aula-11-d556-completo.pdf",
    "pdfs/curso-247136-aula-12-408e-completo.pdf",
    "pdfs/curso-247245-aula-00-prof-antonio-daud-7f34-completo.pdf",
    "pdfs/curso-247245-aula-01-prof-antonio-daud-87bf-completo.pdf",
    "pdfs/curso-247245-aula-02-prof-antonio-daud-somente-pdf-cd42-completo.pdf",
    "pdfs/curso-247245-aula-03-prof-antonio-daud-somente-pdf-cbb3-completo.pdf",
    "pdfs/curso-247245-aula-04-prof-antonio-daud-somente-pdf-b5cc-completo.pdf",
    "pdfs/curso-247245-aula-05-equipe-legislacao-somente-pdf-cef1-completo.pdf",
    "pdfs/Testes de Software - curso-247078-aula-08-profs-diego-carvalho-e-fernando-pedrosa-3c23-completo.pdf"
]"""

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



















































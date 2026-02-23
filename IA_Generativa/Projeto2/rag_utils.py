import os
import sys
# O FAISS é um banco de dados de vetores do Facebook (Meta) que permite buscas ultrarrápidas
from langchain_community.vectorstores import FAISS
# O HuggingFaceEmbeddings transforma frases em listas de números (embeddings)
from langchain_huggingface import HuggingFaceEmbeddings 
# O PyPDFLoader é a ferramenta que consegue "ler" o texto de arquivos PDF
from langchain_community.document_loaders import PyPDFLoader
# O RecursiveCharacterTextSplitter corta textos grandes em pedaços menores (chunks)
from langchain_text_splitters import RecursiveCharacterTextSplitter


class RAGEngine:
    def __init__(self, pdf_paths):
        """
        O construtor da classe: aqui é onde os PDFs são processados e indexados.
        """
        self.docs = []
        # Loop para abrir cada PDF da lista que você passou
        for path in pdf_paths:
            if os.path.exists(path):
                # Carrega o conteúdo do PDF
                loader = PyPDFLoader(path)
                # Adiciona o conteúdo na lista principal de documentos
                self.docs.extend(loader.load())
            else:
                # Avisa se algum arquivo da lista estiver faltando na pasta docs/
                print(f"Arquivo não encontrado: {path}", file=sys.stderr)

        # Configura o "cortador" de texto
        # chunk_size=1000: cada pedaço terá no máximo 1000 caracteres
        # chunk_overlap=200: os pedaços se sobrepõem em 200 caracteres para não perder o contexto entre as divisões
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )  

        # Transforma os PDFs inteiros em centenas de pequenos pedaços (chunks)
        split = text_splitter.split_documents(self.docs)

        # Escolhe o modelo de Inteligência Artificial que vai converter o texto em números
        # O "all-MiniLM-L6-v2" é um modelo leve e excelente para buscas em português/inglês
        embeddings = HuggingFaceEmbeddings(
            model = "sentence-transformers/all-MiniLM-L6-v2"
        )

        # Cria o banco de dados FAISS pegando os pedaços de texto e convertendo em vetores
        self.vector_store = FAISS.from_documents(
            documents=split, embedding=embeddings
        )

        # Transforma o banco de dados em um "Recuperador" (Retriever)
        # search_kwargs={"k": 3} significa que ele sempre trará os 3 pedaços de texto mais relevantes
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        print("RAG Engine inicializando com sucesso.", file=sys.stderr)

    def buscar_contexto(self, query):
        """
        Recebe a pergunta do usuário e busca nos PDFs os trechos mais parecidos.
        """
        # Faz a busca semântica no banco de vetores
        docs = self.retriever.invoker(query)

        # Junta os 3 pedaços encontrados em uma única string, separada por espaços
        return "\n\n".join([doc.page_content for doc in docs])





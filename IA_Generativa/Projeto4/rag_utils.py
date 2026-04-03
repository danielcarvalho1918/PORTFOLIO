import os  # Importa a biblioteca para interagir com o sistema operacional (pastas e caminhos)
import sys  # Importa o sistema para enviar mensagens de log e erros para o terminal
# O FAISS é o motor de busca vetorial; permite salvar e carregar o índice do disco
from langchain_community.vectorstores import FAISS
# O HuggingFaceEmbeddings converte palavras em vetores numéricos (a "linguagem" da IA)
from langchain_huggingface import HuggingFaceEmbeddings 
# O PyPDFLoader é o scanner que extrai o texto bruto de dentro dos seus arquivos PDF
from langchain_community.document_loaders import PyPDFLoader
# O RecursiveCharacterTextSplitter fatia textos longos em pedaços menores e contextuais
from langchain_text_splitters import RecursiveCharacterTextSplitter

class RAGEngine:
    def __init__(self, pdf_paths):
        """
        O construtor da classe: Gerencia a memória de longo prazo e a indexação.
        """
        # Define o nome da pasta física onde o banco de dados vetorial será armazenado
        self.index_path = "faiss_index" 
        
        # Inicializa o modelo de tradução (embedding). Este modelo transforma frases em números.
        # Usamos o 'all-MiniLM-L6-v2' por ser leve, rápido e eficiente para o seu hardware.
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # BLOCO DE VERIFICAÇÃO: Checa se o Senhor já processou esses arquivos anteriormente
        if os.path.exists(self.index_path):
            # Se a pasta existir, o Jarvis carrega o mapa pronto em milissegundos
            print(f" Sensores detectaram índice existente. Carregando mapa de bits...", file=sys.stderr)
            # Carrega o banco de dados do disco para a memória RAM
            self.vector_store = FAISS.load_local(
                self.index_path, 
                self.embeddings, 
                # Permite a leitura de arquivos locais criados pelo próprio Python
                allow_dangerous_deserialization=True 
            )
        else:
            # Se a pasta não existir, iniciamos a 'Leitura de Elite' (processamento pesado)
            print(f" Iniciando indexação primária de {len(pdf_paths)} documentos...", file=sys.stderr)
            self.docs = []  # Lista temporária para armazenar o conteúdo bruto dos PDFs
            
            # Loop que percorre cada caminho de arquivo PDF fornecido na lista
            for path in pdf_paths:
                # Verifica se o arquivo físico realmente existe na pasta 'pdfs'
                if os.path.exists(path):
                    # Inicializa o carregador para o arquivo específico
                    loader = PyPDFLoader(path)
                    # Extrai o texto e adiciona à lista principal de documentos
                    self.docs.extend(loader.load())
                else:
                    # Avisa o Senhor caso algum arquivo da lista tenha sido movido ou deletado
                    print(f" Alerta: Arquivo não encontrado: {path}", file=sys.stderr)

            # Configura o divisor de texto para manter a semântica das leis e apostilas
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,    # Cada pedaço terá no máximo 1000 caracteres
                chunk_overlap=200,   # 200 caracteres de sobra para não cortar frases ao meio
            )  

            # Executa a quebra dos documentos carregados em centenas de pequenos 'chunks'
            split = text_splitter.split_documents(self.docs)

            # Cria o banco de dados vetorial original a partir dos pedaços de texto
            self.vector_store = FAISS.from_documents(
                documents=split, embedding=self.embeddings
            )
            
            # COMANDO CRÍTICO: Salva o banco de dados na pasta local para uso futuro
            self.vector_store.save_local(self.index_path)
            # Confirma que o Senhor não precisará mais esperar este processo na próxima vez
            print(f" Índice salvo com sucesso na pasta '{self.index_path}'.", file=sys.stderr)

        # Transforma o banco de dados em um objeto de recuperação (Retriever)
        # search_kwargs={'k': 5} garante que traremos os 5 trechos mais relevantes por pergunta
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 5})
        # Finaliza a inicialização com o status operacional
        print(" RAG Engine operacional e pronto para combate.", file=sys.stderr)

    def buscar_contexto(self, query):
        """
        Função de combate: Localiza a informação nos PDFs em tempo real.
        """
        # CORREÇÃO DE CIRCUITO: Substituímos 'invoker' por 'invoke' (o comando padrão LangChain)
        # Este comando busca os vetores mais próximos da pergunta do usuário
        docs = self.retriever.invoke(query)

        # Concatena os 3 pedaços de texto encontrados em uma única string formatada
        # Isso será enviado como 'Contexto' para o cérebro do Gemini
        return "\n\n".join([doc.page_content for doc in docs])





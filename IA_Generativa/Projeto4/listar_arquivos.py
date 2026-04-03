import os

# Definição do diretório alvo
pasta_alvo = 'pdfs'

def gerar_caminhos_pdfs(diretorio):
    # Verifica se a pasta existe antes de iniciar a varredura
    if not os.path.exists(diretorio):
        print(f"Alerta, Senhor: A pasta '{diretorio}' não foi localizada.")
        return []

    # Lista os arquivos e concatena o nome da pasta ao nome do arquivo
    # Formato final: "pdfs/nome_do_arquivo.pdf"
    caminhos = [os.path.join(diretorio, f).replace("\\", "/") 
                for f in os.listdir(diretorio) if f.lower().endswith('.pdf')]
    return caminhos

# Execução do protocolo de busca
arquivos_pdf = gerar_caminhos_pdfs(pasta_alvo)

# Exibição formatada para o Senhor copiar para o seu código
print("arquivos_pdf = [")
for i, caminho in enumerate(arquivos_pdf):
    virgula = "," if i < len(arquivos_pdf) - 1 else ""
    print(f'    "{caminho}"{virgula}')
print("]")
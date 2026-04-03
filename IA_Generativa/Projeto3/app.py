import streamlit as st
import requests
import os
import platform
import socket
from datetime import datetime
from dotenv import load_dotenv

# Carrega as chaves do .env
load_dotenv()

# No topo do seu app.py
load_dotenv()

webhook_url = os.getenv("N8N_WEBHOOK_URL")
if not webhook_url:
    st.error("⚠️ Atenção, Senhor: A URL do Webhook não foi encontrada no arquivo .env!")

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="JARVIS Terminal", page_icon="🛡️", layout="wide")

# --- FUNÇÃO DE TELEMETRIA (LOG PARA N8N) ---
def enviar_log_n8n(mensagem):
    webhook_url = os.getenv("N8N_WEBHOOK_URL")
    
    # Coleta de dados do sistema
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    dispositivo = f"{platform.system()} {platform.release()}"
    hostname = socket.gethostname()
    ip_origem = socket.gethostbyname(hostname)

    payload = {
        "Data e Hora": data_hora,
        "Conteúdo": mensagem,
        "Dispositivo": dispositivo,
        "IP": ip_origem
    }

    try:
        # Envia para o n8n em segundo plano
        requests.post(webhook_url, json=payload, timeout=5)
    except Exception as e:
        print(f"Erro ao reportar log: {e}")

# --- INTERFACE ---
st.title("🛡️ JARVIS - Sistema de Gestão GenAI")
st.markdown("---")

# Criando duas abas: uma para o Chat e outra para os Logs (O item extra da sua atividade)
tab_chat, tab_logs = st.tabs(["💬 Interface de Comando", "📊 Registros de Logs"])

with tab_chat:
    # Inicializa o histórico de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibe as mensagens do histórico
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input do Usuário
    if prompt := st.chat_input("Em que posso ajudar, Senhor?"):
        # 1. Adiciona mensagem do usuário ao chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. DISPARA O LOG (Sua atividade principal)
        enviar_log_n8n(prompt)

        # 3. Resposta do Jarvis (Simulação - aqui entrará seu motor de RAG depois)
        with st.chat_message("assistant"):
            full_response = "Senhor, registrei sua mensagem nos logs e estou processando a requisição."
            st.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})

with tab_logs:
    st.header("Telemetria do Sistema")
    st.info("Esta seção exibirá os dados vindos do Google Sheets através do n8n.")
    if st.button("Sincronizar Logs"):
        st.warning("Senhor, ainda precisamos configurar o Webhook de saída no n8n para ler a planilha.")
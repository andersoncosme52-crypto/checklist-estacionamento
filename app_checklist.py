import streamlit as st
import datetime
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="App Checklist de Assunção de Posto",
    page_icon="📋",
    layout="centered"
)

# Título Principal
st.title("📋 Checklist de Assunção de Posto")
st.subheader("Estacionamento - Operação & Supervisão")

# Formulário de Identificação
st.markdown("### 👤 Identificação")
col1, col2 = st.columns(2)
with col1:
    data_selecionada = st.date_input("Data", datetime.date.today())
    operador = st.text_input("Operador Responsável", placeholder="Nome do Operador")
with col2:
    turno = st.selectbox("Turno", ["Manhã", "Tarde", "Noite", "Madrugada"])
    supervisor = st.text_input("Supervisor Responsável", placeholder="Nome do Supervisor")

# Categorias e Itens do Checklist
itens_checklist = {
    "📹 Monitoramento & Câmeras": [
        "Realizar rondas pelas principais câmeras do estacionamento.",
        "Verificar o acesso de entrada e saída de veículos nas câmeras."
    ],
    "💳 Sistemas & Pagamento": [
        "Verificar os IPs das câmeras do sistema de pagamento.",
        "Observar se o sistema apresenta alguma indisponibilidade ou anomalia."
    ],
    "🛠️ Equipamentos & Infraestrutura": [
        "Verificar no Manage o funcionamento geral dos equipamentos.",
        "Conferência do posicionamento, estado e qualidade dos pitocos.",
        "Realizar acesso remoto aos equipamentos de entrada e saída.",
        "Conferir o funcionamento e os horários registrados nos equipamentos."
    ],
    "📶 Redes & Comunicação": [
        "Verificar o funcionamento do Wi-Fi SS2.",
        "Verificar o funcionamento dos VOIPs das entradas.",
        "Verificar o funcionamento dos VOIPs das saídas."
    ],
    "🚨 Segurança": [
        "Verificar o funcionamento do alarme de pânico."
    ]
}

# Dicionário para armazenar as respostas
respostas = {}
observacoes = {}

st.markdown("---")
st.markdown("### 📝 Itens de Verificação")

# Renderização do checklist com rádio de SIM/NÃO e campo de observação por item
for categoria, itens in itens_checklist.items():
    st.markdown(f"#### {categoria}")
    for item in itens:
        # Container para organizar o layout de cada item do checklist
        with st.container():
            col_item, col_status, col_obs = st.columns([5, 2, 3])
            with col_item:
                st.write(item)
            with col_status:
                # Opção de marcar SIM ou NÃO em formato radio horizontal
                status = st.radio(
                    "Status",
                    ["SIM", "NÃO"],
                    key=f"status_{item}",
                    label_visibility="collapsed",
                    horizontal=True
                )
                respostas[item] = status
            with col_obs:
                obs = st.text_input(
                    "Obs",
                    placeholder="Anomalia / Nota",
                    key=f"obs_{item}",
                    label_visibility="collapsed"
                )
                observacoes[item] = obs
        st.markdown("<hr style='margin:0.5rem 0;border-color:#eee;'>", unsafe_allow_html=True)

# Botão de envio e geração de relatório
st.markdown("### 💾 Finalizar Turno")
if st.button("Salvar e Gerar Relatório", type="primary"):
    if not operador or not supervisor:
        st.error("❌ Por favor, preencha o nome do Operador e do Supervisor antes de salvar.")
    else:
        # Criar DataFrame com os resultados
        dados_relatorio = {
            "Item de Verificação": [],
            "Status (Ok?)": [],
            "Observação": []
        }
        for item in respostas:
            dados_relatorio["Item de Verificação"].append(item)
            dados_relatorio["Status (Ok?)"].append(respostas[item])
            dados_relatorio["Observação"].append(observacoes[item])
            
        df = pd.DataFrame(dados_relatorio)
        
        st.success("✅ Checklist salvo com sucesso no sistema!")
        
        # Exibição do resumo para o usuário
        st.markdown("#### Resumo do Turno")
        st.write(f"**Data:** {data_selecionada.strftime('%d/%m/%Y')} | **Turno:** {turno}")
        st.write(f"**Operador:** {operador} | **Supervisor:** {supervisor}")
        st.dataframe(df, hide_index=True)
        
        # Opção de download dos dados em CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Relatório em CSV",
            data=csv,
            file_name=f"checklist_{data_selecionada.strftime('%Y%m%d')}_{turno}.csv",
            mime="text/csv",
        )

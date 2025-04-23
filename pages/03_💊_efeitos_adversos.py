import streamlit as st
from funcoes import *


#Configuração da página
st.set_page_config(page_title="Dashboard para Análise de Medicamentos", layout="wide")
st.title(":blue[Pharma Insights (Efeitos Adversos)]")

with st.sidebar:    
    data = load_data("effects.csv") #Carregamento do conjunto de dados
    classe = st.selectbox(":blue[Selecione a classe terapêutica]", options=data["Therapeutic Class"].dropna().unique(), 
                          help="Selecione a classe terapêutica para\
                             \n visualizar os efeitos adversos dos medicamentos")
    processar = st.button(":blue[Gerar a Nuvem de Palavras]")    
if processar:
        progresso = st.progress(50, text="Carregando a nuvem de palavras... Por favor aguarde um momento.")        
        wordcloud = plot_cloud(data, classe)
        progresso.progress(100, text="Processamento concluído!")
        col1, col2 = st.columns([0.75,0.25], gap="large")        
        with col1:            
            st.subheader(f"Efeitos Colaterais mais frequentes nos \
                            medicamentos da classe :blue[{classe.capitalize()}] ", divider="blue")            
            st.pyplot(wordcloud, use_container_width=True)            
        
        with col2:
            st.subheader(":blue[***Análise de Efeitos Colaterais***]")
            st.markdown("")
            st.markdown("**Monitoramento dos Riscos**")
            st.markdown("*A nuvem de palavras ao lado destaca de forma clara os efeitos adversos mais citados, \
                    facilitando a identificação rápida dos riscos associados ao uso dos medicamentos.*")
            st.subheader(":blue[***Explore e Descubra:***]")
            st.markdown("**Escolha da classe terapêutica**")
            st.markdown("Escolha entre as classes dispomíveis e visualize os efeitos adversos mais comuns associados a cada uma delas. \
                    \n Isso pode ajudar a identificar padrões e tendências, permitindo uma análise mais aprofundada dos riscos associados a cada classe de medicamentos.*")
            st.markdown("*Interaja com o filtro e conheça os sintomas e reações mais recorrentes para embasar decisões clínicas,\
                         otimizando o acompanhamento e a intervenção terapêutica quando necessário.*")            
            
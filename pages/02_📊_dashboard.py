import streamlit as st
from funcoes import *


#Configuração da página
st.set_page_config(page_title="Dashboards para Análises de Medicamentos", layout="wide")
st.title(":blue[Pharma Insights (Dashboard)]")

#Configuração da Barra Lateral
with st.sidebar:
    with st.expander("Expanda para filtrar os medicamentos", expanded=True):
        efeitos = pd.read_csv("effects.csv")
        dados = load_data("medicamentos.csv") #Carregamento do conjunto de dados
        dados = pd.concat((dados, efeitos["n_effects"]), axis=1) #Concatenar os efeitos ao conjunto de dados        
        del efeitos #Deletar o dataframe efeitos para evitar confusão e sobrecarga de memória
        medicamento = st.text_input("Insira um medicamento para analisar", "allegra", help="Digite o nome do medicamento\
                                    \n(ou parte dele) para analisar" ) #Medicamento a ser analisado        
        if not dados["name"].str.contains(medicamento).any(): #Verifica se o medicamento existe no dataframe
            st.error("Medicamento não encontrado nos dados disponíveis. Por favor, tente outro medicamento.")
        dados, dosagens = load_and_process_data(dados, medicamento) #Tratamentos necessários no conjunto de dados        
        filtro_dosagem = st.checkbox(":blue[Selecione para filtrar a dosagem]", help="Insira a dosagem para gerar uma visualização mais focada,\
                                     \n ou deixe em branco para gerar uma viualização de \
                                     \n todos os medicamentos com o mesmo nome.")
        dosagem = None        
        if filtro_dosagem:
            dosagem = st.selectbox("Insira a dosagem (opcional)", dosagens)
    processar = st.button(":blue[Processar]")
  
if processar:        
    #Página exibida caso a dosagem não seja selecionada
    if dosagem is None and medicamento:
        col1, col2 = st.columns([0.6,0.4], gap="large")
        with col1: 
            st.subheader("Análise de Concorrência", divider="blue")
            dados = dados[dados["name"].str.contains(medicamento)]  # Filtrar os dados
            figura = plot_barras_st(dados, "name", "n_substitutes")
            figura.update_traces(text= dados["n_substitutes"], textposition="none",
                                   hovertemplate="Medicamento: %{x}<br>Número de Concorrentes: %{y}", textfont_size=12)
            figura.update_layout(title_text="Número de Concorrentes conhecidos", title_x=0.25, title_font_size=20, 
                                 yaxis_title="Número de Concorrentes", xaxis_title="Medicamento")            
            st.plotly_chart(figura, use_container_width=True)
            st.markdown("**Estes painéis foram projetados para revelar informações essenciais que apoiam decisões mais seguras e precisas " \
            " --- desde a competitividade dos produtos até a gestão de riscos clínicos dos medicamentos**")

        with col2:
            st.subheader("Análise de Efeitos Adversos", divider="blue")
            figura2 = plot_barras_st(dados, "name", "n_effects")
            figura2.update_traces(text= dados["n_effects"], textposition="none",
                                   hovertemplate="Medicamento: %{x}<br>Número de Efeitos Colaterais: %{y}", textfont_size=12)
            figura2.update_layout(title_text="Total de efeitos Colaterais por Medicamento", title_x=0.25, title_font_size=20, 
                                  yaxis_title="Número de Efeitos Colaterais", xaxis_title="Medicamento")            
            st.plotly_chart(figura2, use_container_width=True)            
            st.markdown("**A análise de efeitos colaterais é uma parte essencial do processo de desenvolvimento e monitoramento de medicamentos, " \
            "pois ajuda a identificar e avaliar os riscos associados ao uso do medicamento.**")



        
    else: #Página exibida caso a dosagem seja selecionada       
        dados = filter_dosage(dados, dosagem)  # Filtrar os dados
        if "n_effects" not in dados.columns:  # Verificação da coluna "n_effects"
            raise ValueError("A coluna 'n_effects' não foi encontrada no DataFrame.")
        

        # Dividir o DataFrame caso o filtro resulte em mais de 2 medicamentos
        if len(dados['name'].unique()) >= 5:
            dados = dados.iloc[:4, :]  # Limitar a 5 medicamentos para evitar sobrecarga visual
        if len(dados['name'].unique()) >2 and len(dados['name'].unique()) <=4:
            st.warning("Número de medicamentos filtrados é maior que 2. Dividindo a visualização em duas partes.")        
            
            # Divisão do DataFrame em duas partes
            metade = len(dados) // 2
            dados_parte1 = dados.iloc[:metade, :]
            dados_parte2 = dados.iloc[metade:, :]
            
            # Criar e exibir o primeiro grafo
            grafo1 = criar_grafo(dados_parte1)
            st.subheader("Parte 1")
            st.graphviz_chart(grafo1.source, use_container_width=True)            
            
            # Criar e exibir o segundo grafo
            grafo2 = criar_grafo(dados_parte2)
            st.subheader("Parte 2")
            st.graphviz_chart(grafo2.source, use_container_width=True)
        else:
            # Criar e exibir o grafo normalmente
            grafo = criar_grafo(dados)
            st.graphviz_chart(grafo.source, use_container_width=True)      
        
        st.markdown("<h2 style='text-align: center;'>Descrição da Visualização</h2>", unsafe_allow_html=True)
        st.markdown("O grafo acima ilustra a relação entre os medicamentos e seus concorrentes conhecidos no mercado. \
                    Cada nó representa um medicamento principal, e as arestas os conectam a seus concorrentes \
                    Essa visualização ajuda a entender a dinâmica competitiva e a identificar possíveis alternativas terapêuticas. \
                    Além disso , os efeitos colaterais são exibidos junto ao medicamento principal, permitindo uma análise mais abrangente dos riscos associados. \
                    Essa abordagem facilita a identificação de padrões e tendências, auxiliando na tomada de decisões informadas sobre o uso de medicamentos.")




            


                

    
        

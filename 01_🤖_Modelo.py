import streamlit as st
from funcoes import *
from joblib import load
from numpy import load as load_numpy

#Configuração da página
st.set_page_config(page_title="Análise de Medicamentos", layout="wide")
st.title(":blue[Pharma Insights Modelo]")

#Configuração da Barra Lateral

valores_unicos = {} #Dicionário para armazenar os valores únicos de cada coluna
categoricas = ["Action Class", "Chemical Class", "Habit Forming", "Therapeutic Class", "use0"]
for coluna in categoricas:
    valores_unicos[coluna] = load(f"objects/encoder_{coluna}.joblib")
cross_val = load_numpy("objects/cross_val.npy", allow_pickle=True).item() #Carregamento e exibição do cross_val
st.markdown(f"<div style='font-size: 18px; font-weight: bold'> Acurácia aproximada do Modelo: {cross_val*100:.2f}%</div>", unsafe_allow_html=True)


with st.sidebar:
    with st.expander("Expanda para inserir os dados do novo medicamento", expanded=True):
        dados = load_data("medicamentos_final.csv")
        classe_acao = st.selectbox("Classe de Ação", valores_unicos["Action Class"].classes_, help="Selecione a classe de ação do medicamento")
        classe_quimica = st.selectbox("Classe Química", valores_unicos["Chemical Class"].classes_, help="Selecione a classe química do medicamento")
        formador_habito = st.selectbox("Formador de Hábito", valores_unicos["Habit Forming"].classes_, help="Selecione se o medicamento é formador de hábito")
        classe_terapeutica = st.selectbox("Classe Terapêutica", valores_unicos["Therapeutic Class"].classes_, help="Selecione a classe terapêutica do medicamento")
        uso = st.selectbox("Uso", valores_unicos["use0"].classes_, help="Selecione o uso do medicamento")                        
        dosagem = st.number_input("Dosagem", value=0, help="Selecione a dosagem do medicamento")
        novos_dados = pd.DataFrame({
            "Action Class": classe_acao,
            "Chemical Class": classe_quimica,
            "Habit Forming": formador_habito,            
            "Therapeutic Class": classe_terapeutica,            
            "use0": uso,
            "dosage": dosagem
        }, index=[0])    
    processar = st.button(":blue[Processar os dados]", help="Clique para processar os dados inseridos e gerar a previsão.")
  
if processar:
    progresso = st.progress(50, 
                            text="Processando os dados inseridos... Por favor aguarde um momento.")    
    try:            
        for nome_coluna in categoricas: # Carregamento do encoder para cada coluna categórica
            arquivo_encoder = f'objects/encoder_{nome_coluna}.joblib'
            encoder = load(arquivo_encoder)
            novos_dados[nome_coluna] = encoder.transform(novos_dados[nome_coluna])    
        
        scaler = load("objects/scaler.joblib")  #Carregamento do scaler
        novos_dados["dosage"] = scaler.transform(novos_dados[["dosage"]]) #Transformação da dosagem no dadoframe
        
    except ValueError as erro: #Tratamento de erro caso o valor não esteja no encoder
        st.error(f"Erro ao transformar valor {novos_dados[nome_coluna]}: {erro}")    

    modelo = load("objects/best_model.joblib") #Carregamento do Modelo    
    
    #Geração da previsão e probabilidade
    previsao = modelo.predict(novos_dados)
    previsao_proba = modelo.predict_proba(novos_dados)

    # Exibição dos resultados    
    
    progresso.progress(75, "Gerando Interpretação!")
    figura = Treexplainer(modelo, novos_dados)
    st.markdown("<h1 style='text-align: center; color: #33A6F9'>Interpretação do Modelo</h1>", unsafe_allow_html=True)        
    st_shap(figura, height=200, width=1600) # Plotar o gráfico SHAP    
    progresso.progress(100, "Processamento concluído!")   

    st.markdown("<div style='font-size: 18px; font-weight: bold'>A interpretação do gráfico SHAP fornece uma visão clara" \
            " e objetiva sobre a contribuição de cada variável para a previsão do modelo.\
            Embora simples, essa visualização é extremamente poderosa, pois permite que os usuários compreendam em tempo real como cada variável\
            inserida influenciou na decisão final. Trazendo mais transparência e confiança às previsões do modelo.", unsafe_allow_html=True)
    
    
    st.markdown("<hr style='border: 1px solid #33A6F9; margin-top: 20px; margin-bottom: 20px;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #33A6F9'>Resultados da Previsão:</h1>", unsafe_allow_html=True)    
    dicionario_previsao = {0: "Baixo risco de efeitos adversos", 1: "Alto risco de efeitos adversos"}
    if previsao[0] == 0:
        st.markdown(f"<div style='font-size: 28px; font-weight:bold'>Previsão absoluta: {dicionario_previsao[previsao[0]]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 28px; font-weight: bold'>Probabilidade: {previsao_proba[0][0]*100:.2f}%</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='font-size: 28px; font-weight:bold'>Previsão absoluta:  {dicionario_previsao[previsao[0]]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 28px; font-weight: bold'>Probabilidade: {previsao_proba[0][1]*100:.2f}%</div>", unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("<div style='font-size: 18px; font-weight: bold'>Este indicador representa a probabilidade de ocorrência de efeitos adversos inferiores à média observada,\
    destacando a segurança relativa do medicamento em comparação com outras opções disponíveis no mercado. Embora, de forma geral, todos os medicamentos apresentem\
    algum nível de risco à saúde, aqueles classificados como 'Baixo risco' possuem, mesmo sem comprovação científica definitiva, um potencial promissor para servir\
    de base a futuras pesquisas. Tais estudos podem resultar no desenvolvimento de medicamentos ainda mais seguros, o que é um aspecto relevante a ser levado em consideração. </div>", unsafe_allow_html=True)    
    
    
    


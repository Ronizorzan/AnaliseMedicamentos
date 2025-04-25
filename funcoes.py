"""
Este módulo possui as principais funções utilizadas no projeto e 
tem o objetivo de manter a integridade, a organização,
a limpeza e a performance do código.
As funções foram divididas em seções para facilitar a leitura e a manutenção do código.
"""

import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
import plotly.express as px
import pandas as pd
import numpy as np
from streamlit import cache_resource, cache_data
import streamlit.components.v1 as components
from graphviz import Digraph
import shap


#================================================================================
#Função para cache de dados
@cache_data
def load_data(path):
    """
    Função para carregar os dados do arquivo CSV e armazená-los em cache.
    Parâmetros: path (str): Caminho do arquivo CSV.
    Retorno: data (DataFrame): DataFrame com os dados carregados.
    """
    data = pd.read_csv(path)
    return data

#================================================================================

#Gráficos de Barras para Análise Exploratória
def plot_barras(df, color, maiores):
    """Gráfico de Barras com estilização dinâmica e seleção de
     maiores valores para serem exibidos na análise exploratória.
    (Para conjuntos de dados complexos, com muitos valores únicos)
    
    Parâmetros:
      df (DataFrame): O conjunto de dados de entrada.
      color (str): Nome da cor para plotagem do gráfico
    maiores (int): Quantidade de itens com maior valor a serem selecionados por coluna.
    
    Retorno (fig): Figura do Plotly """
    
    # Configurar o estilo do gráfico
    sns.set_style(style="dark")

    for col in df.columns:
        if df[col].dtype == "object":
            agrupado = df[col].value_counts().nlargest(maiores)

            # Configurar a paleta de cores
            colors = sns.color_palette(str(color), len(agrupado))

            # Criar o gráfico
            fig, ax = plt.subplots()
            bars = ax.bar(agrupado.index, agrupado.values, color=colors)

            # Adicionar rótulos nas barras
            for bar in bars:
                height = bar.get_height()
                ax.annotate('{}'.format(height),
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),  # 3 pontos de deslocamento
                            textcoords="offset points",
                            ha='center', va='bottom')

            # Personalizar os eixos e o título
            ax.set_ylabel(f'Frequência de {col}', fontsize=10, fontweight="bold")
            ax.set_xlabel(f'Valores de {col}', fontsize=10, fontweight="bold")
            ax.set_title(f'Visualização dos {maiores} maiores valores de {col}', fontsize=15, fontweight='bold')
            plt.xticks(rotation=45, ha='right')

            # Remover as bordas desnecessárias e ajustar layout
            sns.despine(left=True, bottom=True)
            plt.tight_layout()
            plt.show()
            
    return fig

#===============================================================================================================


@cache_resource
def load_and_process_data(data, medicamento):
    """Função para filtrar os dados de acordo com o medicamento inserido.
    Parâmetros:
      data (DataFrame): O conjunto de dados de entrada.
      medicamento (str): O nome do medicamento a ser filtrado.
      Retorno: data (DataFrame): DataFrame filtrado com os dados do medicamento.
      dosagens (array): Array com as dosagens disponíveis para o medicamento."""     
    medicamento = str(medicamento).split(" ")[0]  # Transformação do medicamento inserido para string e seleção do primeiro nome        
    nomes = data.loc[:,"name"] #Localização da Coluna Nome
    nomes_separados = nomes.str.split(" ").str[0] #Separação dos Nomes nas colunas do DataFrame
    medicamentos_df = data.loc[nomes_separados.str.contains(medicamento), :] #Localização das Linhas com o nome do medicamento inserido      
    dosagens = medicamentos_df["name"].str.extract(r"(\d+)").fillna(0).astype(int) #Extração das dosagens disponíveis para a caixa de seleção
    data["dosage"] = dosagens
    dosagens = np.unique(dosagens)
    
    return data, dosagens



#================================================================================


#Gráficos de Barras Simples para Análise
def plot_barras_st(df, x, y):
    """Função para criar um gráfico de barras simples usando Plotly Express."""
    if df.shape[0] > 20:
        df = df.iloc[:20, :] # Limitar a 20 linhas para evitar sobrecarga visual
    fig = px.bar(df, x, y, color_discrete_sequence=["#2268EE"])    
    return fig


#============================================================================================================

#Filtro de Dosagens dos Medicamentos
def filter_dosage(medicamentos_df, dosagem):
    """Função para filtrar os medicamentos de acordo com a dosagem inserida.
    Parâmetros:
      medicamentos_df (DataFrame): O conjunto de dados de entrada com uma coluna 'dosage' (dosagem).
      dosagem (int): A dosagem a ser filtrada e retornada no dataframe.
      Retorno: medicamentos_df (DataFrame): DataFrame filtrado com os dados do(s) medicamento(s)."""
    if dosagem is not None:
        medicamentos_df = medicamentos_df.loc[medicamentos_df["dosage"]==dosagem, :]

    return medicamentos_df

#============================================================================================================


#Limitador de Valores Únicos para o modelo de machine learning
def limit_unique_values(df, column, limit):
    """
    Limita os valores únicos de uma coluna, mantendo as top 'limit' categorias e 
    substituindo o restante pelo valor "Others".
    Parâmetros:
        - df (DataFrame): O DataFrame a ser processado.
        - column (str): O nome da coluna a ser limitada.
        - limit (int): O número máximo de categorias a serem mantidas.
    Retorno:
        - df (DataFrame): O DataFrame processado com os valores únicos limitados.        
    """
    value_counts = df[column].value_counts()
    top_values = value_counts.nlargest(limit).index
    df[column] = df[column].apply(lambda x: x if x in top_values else "Others")
    return df


#==========================================================================================================

#Função para geração de Nuvem de Palavras
@cache_resource
def plot_cloud(data, classe, output_file="wordcloud.png"):
    """
    Gera uma nuvem de palavras a partir de um DataFrame filtrado de acordo com a classe terapêutica.
    data (DataFrame): O DataFrame contendo os dados.
    classe (str): A classe terapêutica a ser filtrada e retornada no dataframe.
    output_file (str): O nome de salvamento da nuvem.
    Retorno: fig (Figure): A figura da nuvem de palavras gerada com plotly."""
    # Verificar se a classe está presente na coluna "Therapeutic Class"
    if classe not in data["Therapeutic Class"].unique():
        raise ValueError(f"O valor '{classe}' não foi encontrado no DataFrame.")
    
    # Filtrar os dados pela classe selecionada
    dados_filtrados = data[data["Therapeutic Class"] == classe]
    
    # Combinar o texto de todas as colunas (exceto "Therapeutic Class")
    colunas = [col for col in data.columns if col != "Therapeutic Class"]
    texto_completo = " ".join([
        " ".join(map(str, dados_filtrados[col].dropna().tolist()))
        for col in colunas
    ])
    
    # Converter o texto para minúsculas e dividir em palavras
    palavras = texto_completo.lower()            
        
    # Definir stop words personalizadas e remover do contador
    stops = STOPWORDS.union({"not", "applicable", "not applicable"})    
        
    # Criar a nuvem de palavras com as frequências filtradas
    wordcloud = WordCloud(max_words=50, width=350, height=200, colormap="cool", stopwords=stops, repeat=True).generate(palavras)
    
    # Inicializar a figura, plotar a nuvem e salvar a imagem
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    fig.savefig(output_file, bbox_inches="tight", dpi=600)
    plt.close(fig)
    
    return fig

#==========================================================================================================



# Função para criar o grafo usando Graphviz
def criar_grafo(dataframe):
    """
    Cria um grafo utilizando Graphviz para visualizar medicamentos e substitutos,
    incluindo efeitos colaterais diretamente nos nós do medicamento principal.
    
    Parâmetros:
        - dataframe (pd.DataFrame): Dados contendo colunas name, substitute0...substitute4, n_substitutes, use0, n_effects.
    Retorno:
        - grafo (Digraph): Objeto Graphviz representando o grafo.        
    """
    # Inicializa o grafo
    grafo = Digraph(format='png', engine='fdp', graph_attr={'splines': "neato", "bgcolor": "#0E1117"})
    
    # Loop pelos medicamentos principais e substitutos
    for _, row in dataframe.iterrows():
        medicamento = row['name']
        uso = row['use0']
        n_effects = row['n_effects']
        
        # Medicamento principal com informações adicionais
        grafo.node(
            medicamento, 
            label=f"{medicamento}\nUso: {uso}\nEfeitos Colaterais: {n_effects}", 
            color="blue", 
            shape="oval", 
            style="filled", 
            fillcolor="lightblue"
        )
        
        # Adiciona substitutos ao redor        
        for i in range(5):  # Para substitute0 até substitute4            
            substituto = row[f'substitute{i}']
            if pd.notna(substituto):
                if substituto == "Not Applicable":
                    substituto = "No Substitute Known"
                grafo.node(
                    substituto, 
                    label=substituto, 
                    color="green", 
                    shape="box",
                    style="filled", 
                    fillcolor="grey"
                )
                grafo.edge(
                    medicamento, substituto, 
                    color="white"
                )                
    
    return grafo


#==========================================================================================================


def Treexplainer(model, novos_dados):
    """
    Gera o gráfico de força local usando SHAP (SHapley Additive exPlanations), 
    filtrando as contribuições com valor absoluto abaixo do threshold.

    Parâmetros:
        - model: O modelo de árvore de decisão treinado.
        - novos_dados: O conjunto de dados para o qual os valores SHAP serão calculados.
        - threshold: Valores com magnitude abaixo deste serão definidos como zero.

    Retorno:
        - force_plot: O gráfico de força local gerado com os valores filtrados.
    
    Observação:
        A filtragem pode alterar a soma dos SHAP values e, consequentemente, a previsão final.
        Se for importante preservar a soma original, será necessário ajustar o expected_value.
    """
    # Inicializa o TreeExplainer e calcula os valores SHAP
    tree_explainer = shap.TreeExplainer(model)
    shap_values = tree_explainer.shap_values(novos_dados)    
    #shap.initjs()

    # Se o expected_value for uma lista/array, usamos o primeiro elemento
    if isinstance(tree_explainer.expected_value, (list, tuple, np.ndarray)):
        expected_value = float(tree_explainer.expected_value[0])
        shap_values = shap_values[..., 0]
    else:
        expected_value = float(tree_explainer.expected_value)
    
    
    # Gera o force plot usando os valores filtrados
    force_plot = shap.plots.force(expected_value, shap_values, novos_dados)

    return force_plot


#==========================================================================================================

def st_shap(plot, height=300, width=600):
    """
    Recebe um objeto force_plot do SHAP, converte para HTML e o renderiza no Streamlit.
    
    Parâmetros:
      - plot: Objeto do force plot gerado pelo SHAP.
      - height: Altura do componente HTML exibido.
      - width: Largura do componente HTML exibido.      
    """
    custom_css = """
    <style type="text/css">
      html, body {
          background-color:#2C2E31 !important;
          margin: 0;
          padding: 0;
      }
      /* Caso o container interno possua fundo branco, forçamos outra cor */
      div, svg, .shap-plot {
          background-color: #2C2E31 !important;
      }
    </style>
    """
    shap_html = f"""
    <html>
      <head>
        {shap.getjs()}
        {custom_css}
      </head>
      <body style="margin:0; padding:0;">
        {plot.html()}
      </body>
    </html>
    """
    components.html(shap_html, height=height, width=width)



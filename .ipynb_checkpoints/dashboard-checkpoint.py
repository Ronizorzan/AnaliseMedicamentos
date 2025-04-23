import streamlit as st
from funcoes import *



st.set_page_config(page_title="Dashboard para Visualização de Medicamentos", layout="wide")



with st.sidebar:    
    processar = st.button("Processar")

import streamlit as st
import streamlit.components.v1 as components

# Aplica custom CSS para tema escuro e customização dos elementos do app
st.markdown(
    """
    <style>
        /* Estiliza o fundo e o texto da página */
        body {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        /* Estiliza o conteúdo da barra lateral */
        .css-1d391kg {  /* classe interna de sidebar; pode variar entre versões do Streamlit */
            background-color: #2e2e2e;
        }
        /* Personaliza os botões */
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Título e mensagem principal
st.title("Exifa.net")
st.write("Hi there! I’m Exifa, uma ferramenta de IA feita para ajudar você a entender dados de metadata.")

st.button("How can I use Exifa?")

# Código HTML com JavaScript para visualizar uma rede (usando vis-network)
# Note que aqui usamos uma CDN para carregar a biblioteca vis-network
network_html = """
    <!-- Carrega a biblioteca vis-network a partir de um CDN -->
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <div id="network" style="width: 100%; height: 400px; border: 1px solid #444;"></div>
    <script type="text/javascript">
        // Define os nós da rede
        var nodes = new vis.DataSet([
            {id: 1, label: 'Node 1'},
            {id: 2, label: 'Node 2'},
            {id: 3, label: 'Node 3'},
            {id: 4, label: 'Node 4'},
            {id: 5, label: 'Node 5'}
        ]);

        // Define as conexões (arestas) entre os nós
        var edges = new vis.DataSet([
            {from: 1, to: 2},
            {from: 1, to: 3},
            {from: 2, to: 4},
            {from: 2, to: 5}
        ]);

        // Configura e renderiza o gráfico de rede
        var container = document.getElementById('network');
        var data = {
            nodes: nodes,
            edges: edges
        };
        var options = {
            nodes: {
                color: {
                    background: '#4CAF50',
                    border: '#ffffff',
                    highlight: { background: '#66bb6a', border: '#ffffff' }
                },
                font: { color: '#ffffff' }
            },
            edges: {
                color: { color: '#8a8a8a' }
            }
        };
        var network = new vis.Network(container, data, options);
    </script>
"""

# Incorpora o código HTML/JavaScript no Streamlit
components.html(network_html, height=450)


if processar:
    dados = load_data()
    figura1 = plot_barras_plotly(dados, "name", "substitute0", 20)
    st.plotly_chart(figura1)
    st.write(dados)
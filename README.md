# Pharma Insights Dashboard

O Pharma Insights Dashboard é uma ferramenta de análise interpretável voltada para a indústria farmacêutica. Ela integra um modelo preditivo (baseados em RandomForest) com técnicas de interpretabilidade (usando SHAP – SHapley Additive exPlanations) para auxiliar na identificação dos principais fatores que influenciam os riscos de efeitos adversos dos medicamentos.

## Descrição

Este projeto tem como objetivo:
- Gerar previsões sobre a probabilidade de efeitos adversos.
- Explicar, de maneira visual, como cada variável contribui para a previsão utilizando o force plot do SHAP.

A ferramenta foi desenvolvida em Python, utilizando bibliotecas como [SHAP](https://github.com/slundberg/shap) e [Streamlit](https://streamlit.io/).

## Funcionalidades

- **Análise preditiva:** Utiliza modelos de árvore de decisão (RandomForest) para prever riscos de efeitos adversos.
- **Interpretação dos resultados:** Gera gráficos de força (force plots) com SHAP para demonstrar a contribuição de cada variável.
- **Customização visual:** Ajusta o visual dos gráficos (por exemplo, removendo fundos brancos e aplicando cores que se harmonizam com o layout do dashboard).

## Estrutura do Projeto

- **Modelo.py:** Arquivo principal da aplicação, onde a lógica para carregar o modelo, calcular os valores SHAP e renderizar os gráficos é centralizada.
- **funcoes.py:** Contém todas as funções responsáveis por desempenhar todas as funcionalidades do projeto.
- **pages** Páginas adicionais do projeto com análise de concorrência e efeitos colaterais.
- **requirements.txt:** Lista as dependências do projeto.
- **README.md:** Documentação do projeto.

## Instalação

1. **Pré-requisitos:**  
   - Python 3.7+  
   - Virtualenv (opcional, mas recomendado)

2. **Clone o repositório:**

   ```bash
   git clone <https://github.com/Ronizorzan/AnaliseMedicamentos>
   cd pharma-insights-dashboard

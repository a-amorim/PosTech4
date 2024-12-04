#Importando as bibliotecas
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

dados = pd.read_csv('https://raw.githubusercontent.com/ailaendo/TechChallenge_Fase4/refs/heads/main/Previsao2024.csv')

dados_petroleo = pd.read_csv('https://raw.githubusercontent.com/ailaendo/TechChallenge_Fase4/refs/heads/main/preco_petroleo.csv')


dados_petroleo['Data'] = pd.to_datetime(dados_petroleo['Data'], dayfirst=True)

# Limpar e converter a coluna 'Último' para numérico
dados_petroleo['Último'] = pd.to_numeric(
    dados_petroleo['Último'].str.replace(',', '').str.replace('R$', '', regex=True).str.strip(),
    errors='coerce'
)

# Remover linhas com valores NaN
dados_petroleo.dropna(subset=['Último'], inplace=True)

# Agrupar os dados por mês e calcular a média
preco_mensal = dados_petroleo.set_index('Data').groupby(pd.Grouper(freq='M'))['Último'].mean().reset_index()
preco_mensal['Ano'] = preco_mensal['Data'].dt.year
preco_mensal['Mes'] = preco_mensal['Data'].dt.month_name()

# Criar o gráfico
fig_preco_mensal = px.line(
    preco_mensal,
    x='Mes',
    y='Último',
    color='Ano',
    markers=True,
    title='Preço Mensal'
)

fig_preco_mensal.update_layout(
    yaxis_title='Preço',
    xaxis_title='Mês',
    xaxis=dict(categoryorder='array', categoryarray=pd.date_range(start='2023-01-01', periods=12, freq='M').strftime('%B'))
)

# Agrupar os dados por ano e calcular a média
preco_anual = dados_petroleo.set_index('Data').groupby(pd.Grouper(freq='Y'))['Último'].mean().reset_index()
preco_anual['Ano'] = preco_anual['Data'].dt.year

# Criar o gráfico
fig_preco_anual = px.line(
    preco_anual,
    x='Ano',
    y='Último',
    markers=True,
    title='Preço Anual'
)

fig_preco_anual.update_layout(
    yaxis_title='Preço',
    xaxis_title='Ano',
    xaxis=dict(categoryorder='array', categoryarray=pd.date_range(start='2023-01-01', periods=12, freq='Y').strftime('%B'))
)


# Função para a página "Apresentação"
def pagina_apresentacao():
    st.title('Postech 4 - Análise de preço do petróleo 🛢️')
    st.markdown("""
Este projeto foi desenvolvido por alunos da *FIAP* como parte de um desafio acadêmico. O objetivo foi realizar uma análise detalhada dos dados de petróleo dos últimos anos, com foco no período a partir de *2019*. 
Para garantir a precisão e consistência das análises, utilizamos apenas *anos completos* em nossa abordagem.
""")
    st.markdown("""
### Etapas do Projeto:
1. *Extração de Dados: Os dados de petróleo foram extraídos da base de informações do **IPEA* (Instituto de Pesquisa Econômica Aplicada), que oferece uma visão detalhada sobre o setor de petróleo no Brasil.
2. *Manipulação e Análise com Python: Após a extração, os dados foram manipulados e processados utilizando **Python, por meio de bibliotecas como **pandas* e *matplotlib*, para realizar análises estatísticas e identificar padrões de comportamento ao longo do tempo.
3. *Visualização de Dados: As descobertas foram então apresentadas por meio de **visualizações interativas, utilizando as plataformas **PowerBI* e *Streamlit*. Essas ferramentas possibilitam uma experiência mais rica e dinâmica na exploração dos dados, oferecendo gráficos e dashboards para facilitar a compreensão dos insights gerados.
""")
    st.write("""
Este projeto tem como objetivo fornecer uma visão clara e acessível sobre as tendências e mudanças no setor de petróleo nos últimos anos, com base em dados concretos e análises técnicas detalhadas.
""")

# Função para a página "Visualização dos Dados"
def pagina_visualizacao():
    st.title("Visualização dos Dados 📈")
    st.write("Neste projeto, realizamos uma análise detalhada dos valores do petróleo ao longo dos últimos anos, com foco nos dados anuais até o final de 2023. A partir desses dados históricos, investigamos tendências e padrões de comportamento dos preços do petróleo, considerando os diversos fatores econômicos e geopolíticos que impactaram o mercado global. Para aprofundar ainda mais a análise, utilizamos o modelo Prophet do Python para realizar previsões de preços do petróleo para os primeiros três meses de 2024. O Prophet é um modelo de previsão robusto, desenvolvido pelo Facebook, que se destaca por sua capacidade de lidar com séries temporais complexas e sazonalidades, oferecendo previsões precisas, mesmo em cenários de dados com variações inesperadas. Essas previsões fornecem insights valiosos para a compreensão das possíveis flutuações no mercado de petróleo nos próximos meses, ajudando a antecipar mudanças nas tendências e permitir uma melhor tomada de decisão em relação a investimentos e estratégias comerciais.")
    st.plotly_chart(fig_preco_anual)
    
    st.markdown("### Tabela de Previsão de Preço do Petróleo")
    st.write("Previsão para o primeiro trimestre de 2024")
    st.dataframe(dados)
        

# Função para a página "Análise anual"
def pagina_ideias():
    st.title("Análise anual 🔍")
    dados_petroleo['Ano'] = dados_petroleo['Data'].dt.year
    anos_disponiveis = sorted(dados_petroleo['Ano'].unique())
    ano_selecionado = st.selectbox("Selecione o ano:", anos_disponiveis)
    dados_filtrados = dados_petroleo[dados_petroleo['Ano'] == ano_selecionado]
    preco_mensal = dados_filtrados.set_index('Data').groupby(pd.Grouper(freq='M'))['Último'].mean().reset_index()
    preco_mensal['Mes'] = preco_mensal['Data'].dt.month_name()
    fig_preco_mensal = px.line(
    preco_mensal,
    x='Mes',
    y='Último',
    markers=True,
    title=f'Preço Mensal - Ano {ano_selecionado}')
    fig_preco_mensal.update_layout(
    yaxis_title='Preço',
    xaxis_title='Mês',
    xaxis=dict(categoryorder='array', categoryarray=pd.date_range(start='2023-01-01', periods=12, freq='M').strftime('%B'))
)
    st.plotly_chart(fig_preco_mensal)

    if ano_selecionado == 2020:
        st.markdown("### Análise do ano de 2020:")
        st.write("Em 2020, o mercado de petróleo sofreu uma queda histórica devido à pandemia de COVID-19, com uma redução drástica na demanda global. O impacto foi profundo, com preços caindo a níveis recordes.")
    elif ano_selecionado == 2021:
        st.markdown("### Análise do ano de 2021:")
        st.write("Em 2021, o mercado de petróleo começou a se recuperar da queda de 2020, impulsionado pela recuperação gradual da economia global. A demanda aumentou e os preços começaram a subir novamente.")
    elif ano_selecionado == 2022:
        st.markdown("### Análise do ano de 2022:")
        st.write("Em 2022, o mercado de petróleo foi fortemente impactado pela guerra entre a Rússia e a Ucrânia, o que causou uma grande volatilidade nos preços devido a incertezas quanto ao fornecimento.")
    elif ano_selecionado == 2023:
        st.markdown("### Análise do ano de 2023:")
        st.write("Em 2023, o mercado de petróleo se estabilizou, mas ainda sob o impacto da guerra na Ucrânia e das políticas de produção da OPEC. O preço do petróleo variou, mas sem grandes quedas ou aumentos bruscos.")
    else:
        st.markdown("### Análise do ano de 2019:")
        st.write("2019 foi um ano de preços de petróleo relativamente estáveis, com aumentos ocasionais devido a choques de oferta e incertezas geopolíticas. A produção de petróleo dos EUA e os cortes da OPEC foram fatores chave para o comportamento do mercado durante o ano")
   
# Menu de navegação
pagina = st.sidebar.radio("🏠 Menu", ["Apresentação", "Visualização dos Dados", "Análise anual"])

# Condicional para exibir o conteúdo correto conforme a página selecionada
if pagina == "Apresentação":
    pagina_apresentacao()

elif pagina == "Visualização dos Dados":
    pagina_visualizacao()

elif pagina == "Análise anual":
    pagina_ideias()
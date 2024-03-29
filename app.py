import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

@st.cache
def gerar_df():
    dataframe = pd.read_excel(
        io="C:\\Users\\30783\\OneDrive\\Área de Trabalho\\python\\CouroXDolar.xlsx",
        engine="openpyxl",
        sheet_name="Planilha1",
        usecols="A:D",
        nrows=283
    )
    return dataframe

df_global = gerar_df()

colunasuteis = ['mes', 'ano', 'ValorCouro', 'ValorDolar']
df_global = df_global[colunasuteis]
df_global['ano'] = df_global['ano'].astype(str)
df_global['mes'] = df_global['mes'].astype(str)
df_global['mes'] = df_global['mes'].str.zfill(2)
df_global['ano_mes'] = df_global['ano'] + '-' + df_global['mes']

with st.sidebar:
    st.subheader('Precificação Couro x Dolar')
    logo_teste = Image.open("C:\\Users\\30783\\OneDrive\\Área de Trabalho\\python\\logo.jpg")
    st.image(logo_teste, use_column_width=True)
    st.subheader('Seleção de Filtros')
    anos = ['Todos os anos'] + list(df_global['ano'].unique())
    ano_selecionado = st.selectbox('Escolha um ano:', anos)

    if ano_selecionado == 'Todos os anos':
        df_filtrado = df_global
    else:
        df_filtrado = df_global[df_global['ano'] == ano_selecionado]


chart_couro = alt.Chart(df_filtrado).mark_line().encode(
    x=alt.X('ano_mes:T', title='Ano e Mês'),
    y=alt.Y('ValorCouro', title='Preço do Couro'),
    tooltip=['ano_mes', 'ValorCouro']
).properties(
    width=800,
    height=300,
    title=f'Evolução do Preço do Couro ({ano_selecionado if ano_selecionado != "Todos os anos" else "Todos os anos"})'
)

chart_dolar = alt.Chart(df_filtrado).mark_bar().encode(
    x=alt.X('ano_mes:T', title='Ano e Mês'),
    y=alt.Y('ValorDolar', title='Preço do Dólar'),
    color=alt.value('orange'),
    tooltip=['ano_mes', 'ValorDolar']
).properties(
    width=800,
    height=300,
    title=f'Evolução do Preço do Dólar ({ano_selecionado if ano_selecionado != "Todos os anos" else "Todos os anos"})'
)


st.altair_chart(chart_couro, use_container_width=True)
st.altair_chart(chart_dolar, use_container_width=True)

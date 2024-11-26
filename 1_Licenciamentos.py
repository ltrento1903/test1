import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Licenciamentos Históricos 🚗")

# Carregar os dados
df = pd.read_excel(r"C:\Tablets\Automoveis.xlsx")
df['Mês'] = pd.to_datetime(df['Mês'])  # Converte para datetime

col1, col2 = st.columns([1,1], gap="large")

with col1:
    st.subheader("Licenciamentos Automóveis - 1990 à 2024")
    st.dataframe(df)


with col2:
    st.subheader("Licenciamentos Automóveis - 1990 à 2024")
    fig = px.line(
        df,
        x="Mês",
        y="AUTOMÓVEIS",
        title="Evolução dos Licenciamentos de Automóveis"
    )
    fig.update_layout(
        xaxis_title="Mês",
        yaxis_title="Número de Licenciamentos",
        title_font_size=20
    )
    st.plotly_chart(fig)


import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from statsmodels.tsa.seasonal import seasonal_decompose

st.title("Análises de Licenciamentos")

# Carregar os dados
df = pd.read_excel(r"C:\Tablets\Automoveis.xlsx", index_col=0, parse_dates=True)

col1, col2=st.columns([2,2])

with col1:
    result = seasonal_decompose(df['AUTOMÓVEIS'], model='additive')


    fig_decompose = go.Figure()
    fig_decompose.add_trace(go.Scatter(x=df.index, y=df['AUTOMÓVEIS'], mode='lines', name='Original'))
    fig_decompose.add_trace(go.Scatter(x=df.index, y=result.trend, mode='lines', name='Tendência'))
    fig_decompose.add_trace(go.Scatter(x=df.index, y=result.seasonal, mode='lines', name='Sazonalidade'))
    fig_decompose.update_layout(title="Decomposição Sazonal", xaxis_title="Data", yaxis_title="Valor")
    st.plotly_chart(fig_decompose)

with col2:

# Boxplot e histograma
    fig_box = px.box(df, y="AUTOMÓVEIS", title="Distribuição dos Licenciamentos (Boxplot)")
    fig_hist = px.histogram(df, x="AUTOMÓVEIS", title="Distribuição dos Licenciamentos (Histograma)")

    st.plotly_chart(fig_box)
    st.plotly_chart(fig_hist)

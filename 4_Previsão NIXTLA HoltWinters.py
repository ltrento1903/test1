import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsforecast import StatsForecast
from statsforecast.models import HoltWinters
import streamlit as st

# Título
st.header("Previsão para Licenciamentos de Automóveis usando NIXTLA Holt Winters")

# Configuração de layout para colunas
col1, col2, col3 = st.columns([2, 5, 5], gap='large')

# **Coluna 1: Pré-processamento e testes estatísticos**
with col1:
    # Leitura dos dados
    file_path = r"C:\Tablets\Automoveis.xlsx"
    df_1 = pd.read_excel(file_path)

    # Ajuste de colunas
    df_1.columns = ["ds", "y"]
    df_1["unique_id"] = "1"
    df_1["ds"] = pd.to_datetime(df_1["ds"])
    df_1 = df_1[["unique_id", "ds", "y"]]

    # Teste Dickey-Fuller
    def augmented_dickey_fuller_test(series, column_name):
        dftest = adfuller(series.dropna(), autolag="AIC")
        dfoutput = pd.Series(dftest[0:4], index=["Test Statistic", "p-value", "No Lags Used", "Number of Observations Used"])
        for key, value in dftest[4].items():
            dfoutput[f"Critical Value ({key})"] = value
        st.write(f"Resultados do Teste Dickey-Fuller para {column_name}:")
        st.write(dfoutput)
        if dftest[1] <= 0.05:
            st.write("Conclusão: A hipótese nula foi rejeitada. Os dados são estacionários.")
        else:
            st.write("Conclusão: A hipótese nula não pode ser rejeitada. Os dados não são estacionários.")

    augmented_dickey_fuller_test(df_1["y"], "y")

    # ACF e PACF
    def plot_acf_pacf(series, lags=30):
        acf_values = acf(series.dropna(), nlags=lags)
        pacf_values = pacf(series.dropna(), nlags=lags)

        fig_acf = go.Figure()
        fig_acf.add_trace(go.Bar(x=list(range(len(acf_values))), y=acf_values, name="ACF"))
        fig_acf.update_layout(
            title="Função de Autocorrelação (ACF)",
            xaxis_title="Lag",
            yaxis_title="ACF",
            template="plotly_dark"
        )

        fig_pacf = go.Figure()
        fig_pacf.add_trace(go.Bar(x=list(range(len(pacf_values))), y=pacf_values, name="PACF"))
        fig_pacf.update_layout(
            title="Função de Autocorrelação Parcial (PACF)",
            xaxis_title="Lag",
            yaxis_title="PACF",
            template="plotly_dark"
        )

        return fig_acf, fig_pacf

    fig_acf, fig_pacf = plot_acf_pacf(df_1["y"])
    st.plotly_chart(fig_acf)
    st.plotly_chart(fig_pacf)

# **Coluna 2: Visualização e decomposição**
with col2:
    # Plot da série temporal
    fig = px.line(df_1, x="ds", y="y", title="Dados de Licenciamento", labels={"ds": "Data", "y": "Valores"})
    st.write('Licenciamentos Automóveis')
    st.plotly_chart(fig)

    # Decomposição sazonal
    decompose_add = seasonal_decompose(df_1.set_index("ds")["y"], model="additive", period=12)
    add_fig = go.Figure()
    add_fig.add_trace(go.Scatter(y=decompose_add.trend, mode="lines", name="Tendência"))
    add_fig.add_trace(go.Scatter(y=decompose_add.seasonal, mode="lines", name="Sazonalidade"))
    add_fig.add_trace(go.Scatter(y=decompose_add.resid, mode="lines", name="Resíduo"))
    add_fig.update_layout(title="Decomposição Sazonal (Aditiva)", template="plotly_dark")
    st.plotly_chart(add_fig)

# **Coluna 3: Previsão e métricas**
with col3:
    # Previsão com StatsForecast
    season_length = 12
    horizon = 12

    models = [
        HoltWinters(season_length=season_length, error_type="A", alias="Add"),
        HoltWinters(season_length=season_length, error_type="M", alias="Multi"),
    ]

    sf = StatsForecast(df=df_1, models=models, freq="M", n_jobs=-1)
    forecast = sf.forecast(horizon)
    st.write('Previsão Holt Winters Aditiva e Multiplicativa:')
    st.dataframe(forecast, height=300)

    # Métricas de avaliação
    def calculate_metrics(actual, predicted):
        mse = np.mean((actual - predicted) ** 2)
        mae = np.mean(np.abs(actual - predicted))
        mape = np.mean(np.abs((actual - predicted) / actual)) * 100
        rmse = np.sqrt(mse)
        bias = np.mean(predicted - actual)
        bias_rate = bias / np.mean(actual) * 100
        return mse, mae, mape, rmse, bias, bias_rate

    metrics_list = []
    for model in ['Add', 'Multi']:
        predicted = forecast[model].values[:horizon]
        actual = df_1['y'].iloc[-horizon:].values
        mse, mae, mape, rmse, bias, bias_rate = calculate_metrics(actual, predicted)
        metrics_list.append({
            'Model': model,
            'MSE': mse,
            'MAE': mae,
            'MAPE': mape,
            'RMSE': rmse,
            'Bias': bias,
            'Bias Rate': bias_rate
        })

    metrics_df = pd.DataFrame(metrics_list)
    st.write("Métricas dos Modelos:")
    st.dataframe(metrics_df.style.highlight_min(axis=0, subset=metrics_df.columns[1:]))

    # Visualização da previsão
    fig = go.Figure()
    for model in ['Add', 'Multi']:
        fig.add_trace(go.Scatter(
            x=forecast['ds'],
            y=forecast[model],
            mode='lines+markers',
            name=model
        ))
    fig.add_trace(go.Scatter(
        x=df_1['ds'],
        y=df_1['y'],
        mode='lines',
        name='Valores Reais',
        line=dict(color='black')
    ))
    fig.update_layout(
        title='Previsões de Séries Temporais',
        xaxis_title='Data',
        yaxis_title='Valores',
        template='plotly_white'
    )
    st.plotly_chart(fig)

# Importação de bibliotecas necessárias
import pandas as pd
import numpy as np
import streamlit as st
from statsmodels.tsa.api import ExponentialSmoothing
from sklearn.metrics import mean_squared_error, mean_absolute_error
from prophet import Prophet

st.title('Previsão para Licenciamentos Automóveis por meio do Prophet (sazonalidade Aditiva e Multiplicativa)')

col1, col2, col3 =st.columns([4, 8, 8], gap='large')

# Funções para calcular métricas
def calculate_metrics(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    bias = np.mean(y_pred - y_true)
    bias_rated = np.mean((y_pred - y_true) / y_true) * 100

    return mse, mae, rmse, mape, bias, bias_rated

with col1:    

# Leitura dos dados
    file_path = r"C:\Tablets\Automoveis.xlsx"
    df= pd.read_excel(file_path)    

   # Convertendo coluna de datas para datetime
    df['Mês'] = pd.to_datetime(df['Mês'])

# Preparando o DataFrame para o Prophet
    df['ds'] = df['Mês']
    df['y'] = df['AUTOMÓVEIS']
    df_novo = df[['ds', 'y']]
    

# Criando e treinando o modelo Prophet
    modelo = Prophet(seasonality_mode='additive')
    modelo.fit(df_novo)

# Criando DataFrame de previsões
    dataFramefuturo = modelo.make_future_dataframe(periods=12, freq='ME')
    forecast = modelo.predict(dataFramefuturo)  
    
    
    modelo.plot_components(forecast, figsize=(10,6));

# Filtrando previsões para as datas disponíveis no conjunto original (dados históricos)
    forecast_historical = forecast[forecast['ds'].isin(df['ds'])]
    st.write('Filtrando Previsões para os dados histórico')
    st.dataframe(forecast_historical, height=300)

with col2:
    st.write('Previsão licenciamentos automóveis por meio do Prophet (sazonalidade aditiva)')
    st.dataframe(forecast, height=300)

# Extraindo valores reais e previstos para comparação
    y_true = df['y'].values
    y_pred = forecast_historical['yhat'].values
  

    import plotly.graph_objects as go

# Criando a figura
    fig = go.Figure()

# Dados reais
    fig.add_trace(go.Scatter(
        x=df['ds'], 
        y=y_true, 
        mode='lines+markers', 
        name='Real', 
        marker=dict(color='blue')
    ))

# Previsão futura
    fig.add_trace(go.Scatter(
        x=forecast['ds'], 
        y=forecast['yhat'], 
        mode='lines', 
        name='Previsão Futura', 
        line=dict(color='orange', dash='dash')
    ))

# Previsão histórica
    fig.add_trace(go.Scatter(
        x=forecast_historical['ds'], 
        y=y_pred, 
        mode='lines', 
        name='Previsão Histórica', 
        line=dict(color='green')
    ))

# Layout do gráfico
    fig.update_layout(
        title='Comparação de Dados Reais e Previsões - Sazonalidade Aditiva',
        xaxis_title='Data',
        yaxis_title='Licenciamentos Automóveis',
        legend_title='Legenda',
        template='plotly_white'  # Estilo limpo para o gráfico
    )

    st.plotly_chart(fig)

# Calculando as métricas
    mse, mae, rmse, mape, bias, bias_rated = calculate_metrics(y_true, y_pred)

     # Exibindo métricas em formato de caixas individuais
    st.write('Metricas Performance Prophet sazonalidade aditiva')
    st.metric("MSE", f"{mse:.2f}")
    st.metric("MAE", f"{mae:.2f}")
    st.metric("RMSE", f"{rmse:.2f}")
    st.metric("MAPE", f"{mape:.2f}%")
    st.metric("Bias", f"{bias:.2f}")
    st.metric("Bias Rated", f"{bias_rated:.2f}%")


# Exibindo os resultados
    print(f"MSE: {mse:.2f}")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"MAPE: {mape:.2f}%")
    print(f"Bias: {bias:.2f}")
    print(f"Bias Rated: {bias_rated:.2f}%")

    from plotly.subplots import make_subplots

# Extração dos componentes do forecast
    trend = forecast[['ds', 'trend']]
    seasonalities = forecast[['ds', 'yearly', 'weekly']] if 'weekly' in forecast.columns else forecast[['ds', 'yearly']]

# Criando subplots para os componentes
    fig_comp = make_subplots(
        rows=3, cols=1,
        subplot_titles=("Tendência", "Sazonalidade Anual", "Sazonalidade Semanal" if 'weekly' in forecast.columns else None),
        shared_xaxes=True
    )

# Tendência
    fig_comp.add_trace(
    go.Scatter(x=trend['ds'], y=trend['trend'], mode='lines', name='Tendência', line=dict(color='blue')),
    row=1, col=1
    )
    
# Sazonalidade Anual
    fig_comp.add_trace(
        go.Scatter(x=seasonalities['ds'], y=seasonalities['yearly'], mode='lines', name='Sazonalidade Anual', line=dict(color='green')),
        row=2, col=1
    )

# Sazonalidade Semanal (se disponível)
    if 'weekly' in forecast.columns:
        fig_comp.add_trace(
            go.Scatter(x=seasonalities['ds'], y=seasonalities['weekly'], mode='lines', name='Sazonalidade Semanal', line=dict(color='purple')),
            row=3, col=1
        )

# Layout do gráfico
    fig_comp.update_layout(
        height=800,
        title_text="Componentes do Modelo Prophet",
        xaxis_title="Data",
        yaxis_title="Valor",
        showlegend=False
    )

    st.plotly_chart(fig_comp)

with col3:

# Criando e treinando o modelo Prophet
    modelo = Prophet(seasonality_mode='multiplicative')
    modelo.fit(df_novo)

# Criando DataFrame de previsões
    dataFramefuturo_m = modelo.make_future_dataframe(periods=12, freq="ME")
    forecast_m = modelo.predict(dataFramefuturo_m)    
    st.write('Previsão licenciamentos automóveis por meio do Prophet (sazonalidade multiplicativa)')
    st.dataframe(forecast_m, height=300)


# Filtrando previsões para as datas disponíveis no conjunto original (dados históricos)
    forecast_historical = forecast[forecast['ds'].isin(df['ds'])]   

    import plotly.graph_objects as go

# Criando a figura
    fig_m = go.Figure()

# Dados reais
    fig_m.add_trace(go.Scatter(
        x=df['ds'], 
        y=y_true, 
        mode='lines+markers', 
        name='Real', 
        marker=dict(color='blue')
    ))

# Previsão futura
    fig_m.add_trace(go.Scatter(
        x=forecast_m['ds'], 
        y=forecast_m['yhat'], 
        mode='lines', 
        name='Previsão Futura', 
        line=dict(color='orange', dash='dash')
    ))

# Previsão histórica
    fig_m.add_trace(go.Scatter(
        x=forecast_historical['ds'], 
        y=y_pred, 
        mode='lines', 
        name='Previsão Histórica', 
        line=dict(color='green')
    ))

# Layout do gráfico
    fig_m.update_layout(
        title='Comparação de Dados Reais e Previsões - Sazonalidade Multiplicativa',
        xaxis_title='Data',
        yaxis_title='Licenciamentos Automóveis',
        legend_title='Legenda',
        template='plotly_white'  # Estilo limpo para o gráfico
    )

# Exibindo o gráfico
    st.plotly_chart(fig_m)


# Extraindo valores reais e previstos para comparação
    y_true = df['y'].values
    y_pred = forecast_historical['yhat'].values

# Calculando as métricas
    mse, mae, rmse, mape, bias, bias_rated = calculate_metrics(y_true, y_pred)

# Exibindo os resultados
    print(f"MSE: {mse:.2f}")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"MAPE: {mape:.2f}%")
    print(f"Bias: {bias:.2f}")
    print(f"Bias Rated: {bias_rated:.2f}%")
    st.write('Metricas Performance Prophet sazonalidade multiplicativa')
    st.metric("MSE", f"{mse:.2f}")
    st.metric("MAE", f"{mae:.2f}")
    st.metric("RMSE", f"{rmse:.2f}")
    st.metric("MAPE", f"{mape:.2f}%")
    st.metric("Bias", f"{bias:.2f}")
    st.metric("Bias Rated", f"{bias_rated:.2f}%")


    from plotly.subplots import make_subplots

# Extração dos componentes do forecast
    trend = forecast[['ds', 'trend']]
    seasonalities = forecast[['ds', 'yearly', 'weekly']] if 'weekly' in forecast.columns else forecast[['ds', 'yearly']]

# Criando subplots para os componentes
    fig_cm = make_subplots(
        rows=3, cols=1,
        subplot_titles=("Tendência", "Sazonalidade Anual", "Sazonalidade Semanal" if 'weekly' in forecast.columns else None),
        shared_xaxes=True
    )

# Tendência
    fig_cm.add_trace(
        go.Scatter(x=trend['ds'], y=trend['trend'], mode='lines', name='Tendência', line=dict(color='blue')),
        row=1, col=1
    )

# Sazonalidade Anual
    fig_cm.add_trace(
        go.Scatter(x=seasonalities['ds'], y=seasonalities['yearly'], mode='lines', name='Sazonalidade Anual', line=dict(color='green')),
        row=2, col=1
    )

# Sazonalidade Semanal (se disponível)
    if 'weekly' in forecast.columns:
        fig_cm.add_trace(
            go.Scatter(x=seasonalities['ds'], y=seasonalities['weekly'], mode='lines', name='Sazonalidade Semanal', line=dict(color='purple')),
            row=3, col=1
        )

# Layout do gráfico
    fig_cm.update_layout(
        height=800,
        title_text="Componentes do Modelo Prophet",
        xaxis_title="Data",
        yaxis_title="Valor",
        showlegend=False
    )

   


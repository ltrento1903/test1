import pandas as pd
import numpy as np
import plotly.graph_objects as go
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, AutoETS, AutoTheta, AutoCES
import streamlit as st

st.header('Previsão Automóveis usando NIXTLA Automatic Time Series Forecasting: AutoArima, AutoETS, AutoTheta, AutoCES')

col1, col2, col3 = st.columns([2,3,3], gap='large')

# Ler os dados do Excel
df = pd.read_excel(r"C:\Tablets\Automoveis.xlsx")

# Renomear colunas para o formato esperado e adicionar ID único
df = df.rename(columns={"Mês": "ds", "AUTOMÓVEIS": "y"})
df['unique_id'] = 'serie_1'  # Valor fixo para uma única série temporal

# Garantir que a coluna de datas está no formato datetime
df['ds'] = pd.to_datetime(df['ds'])

with col1:

    st.write('Dataframe estruturado para rodar Nixtla')
    st.dataframe(df, height=300)

# Configurações
    season_length = 12  # Sazonalidade (12 meses para dados mensais)
    horizon = 12        # Horizonte de previsão (12 meses)

# Lista de modelos de previsão
    models = [
        AutoARIMA(season_length=season_length),
        AutoETS(season_length=season_length),
        AutoTheta(season_length=season_length),
        AutoCES(season_length=season_length),
    ]

# Instanciar a classe StatsForecast
    sf = StatsForecast(
        models=models,
        freq='M',  # Frequência mensal
        n_jobs=-1  # Utilizar todos os núcleos disponíveis
    )

# Gerar previsões
    forecast = sf.forecast(df=df, h=horizon)

with col2:

   st.write('Previsão Autoarima, AutoETS, AutoTheta e CES')
   st.dataframe(forecast, height=300)

   st.markdown('''Divergências e Padrões Específicos
•	AutoARIMA: Geralmente mais alto no início e no fim do período, com previsões mais altas em outubro de 2024 e valores intermediários na maioria dos meses.
•	AutoETS: Alterna entre previsões conservadoras (fim de 2024 e início de 2025) e otimistas (meados de 2025).
•	AutoTheta: Exibe um padrão de crescimento mais agressivo em meados de 2025, sendo o mais otimista em termos de valores máximos.
•	CES: Relativamente estável, com menos oscilação ao longo dos meses.
________________________________________
Análise de Consistência e Estabilidade
•	CES e AutoTheta têm maior proximidade em diversos meses, sugerindo que podem capturar tendências similares do conjunto de dados.
•	AutoETS apresenta maior variabilidade nas previsões ao longo do período, com valores significativamente altos ou baixos dependendo do mês.
•	AutoARIMA tem previsões mais regulares e um desvio padrão menor em comparação com os outros modelos.
________________________________________
Escolha do Modelo
A escolha do modelo ideal dependerá dos objetivos do usuário:
•	Se estabilidade for mais importante: CES é o mais adequado.
•	Se o objetivo for capturar picos de crescimento: AutoTheta pode ser a melhor opção.
•	Se previsões conservadoras forem desejadas: AutoETS é apropriado.
•	Se for necessário equilíbrio entre conservadorismo e otimismo: AutoARIMA se destaca.
________________________________________

''')

# Garantir que a previsão inclua apenas as colunas necessárias
forecast = forecast.reset_index()

# Selecionar valores reais (observados) correspondentes às datas previstas
# Neste caso, consideramos que a previsão começa após a última data do conjunto original
forecast['ds'] = pd.to_datetime(forecast['ds'])

# Função para calcular métricas
def calculate_metrics(actual, predicted):
        mse = np.mean((actual - predicted) ** 2)
        mae = np.mean(np.abs(actual - predicted))
        mape = np.mean(np.abs((actual - predicted) / actual)) * 100
        rmse = np.sqrt(mse)
        bias = np.mean(predicted - actual)
        bias_rate = bias / np.mean(actual) * 100
        return mse, mae, mape, rmse, bias, bias_rate

# Calcular métricas para cada modelo
metrics_list = []
for model in ['AutoARIMA', 'AutoETS', 'AutoTheta', 'CES']:
        # A previsão para o modelo precisa ser comparada com os valores reais (observados)
        predicted = forecast[model].values
        # Não temos valores reais para o horizonte de previsão, então o cálculo será feito com base apenas nas previsões
        mse, mae, mape, rmse, bias, bias_rate = calculate_metrics(df['y'].iloc[-horizon:], predicted)
        metrics_list.append({
            'Model': model,
            'MSE': mse,
            'MAE': mae,
            'MAPE': mape,
            'RMSE': rmse,
            'Bias': bias,
            'Bias Rate': bias_rate
        })

# Criar DataFrame com métricas
metrics_df = pd.DataFrame(metrics_list)

with col3:
   st.write("Medidas de Performance")
   st.dataframe(metrics_df.style.highlight_min(axis=0, subset=metrics_df.columns[1:]))

# Visualizar as métricas
print(metrics_df)

# Criar gráfico com Plotly
fig = go.Figure()

# Adicionar previsões de cada modelo
for model in ['AutoARIMA', 'AutoETS', 'AutoTheta', 'CES']:
        fig.add_trace(go.Scatter(
            x=forecast['ds'],
            y=forecast[model],
            mode='lines+markers',
            name=model
        ))

# Adicionar série temporal original (valores reais)
fig.add_trace(go.Scatter(
        x=df['ds'],
        y=df['y'],
        mode='lines',
        name='Valores Reais',
        line=dict(color='black')
    ))

# Configurações do layout
fig.update_layout(
        title='Previsões de Séries Temporais por Modelo',
        xaxis_title='Data',
        yaxis_title='Previsão',
        legend_title='Modelos',
        template='plotly_white'
    )

# Exibir o gráfico
with col3:
    st.write('Gráfico Previsão')
    st.plotly_chart(fig)
    st.markdown('''Comparação Geral e Escolha do Modelo 
    Com base nas métricas:
    AutoETS:
    Melhor desempenho geral em MSE, MAE, MAPE, RMSE e Bias.
    Indicado para previsões mais precisas e balanceadas.
    CES:
    Segunda melhor opção, com resultados consistentes, mas inferiores ao AutoETS.
    AutoARIMA:
    Bom em termos absolutos, mas apresenta maior viés e penalização por desvios grandes.
    AutoTheta:
    Menos eficiente, com maior viés e erros absolutos, indicando que não é a melhor escolha para este conjunto de dados.
    Recomendações
    Modelo preferido: AutoETS, devido ao menor erro geral e viés.
    Se estabilidade adicional for necessária, o CES pode ser uma boa alternativa.
    Os outros modelos podem ser úteis em cenários específicos, mas não são as melhores opções globais para este caso.
    ''')



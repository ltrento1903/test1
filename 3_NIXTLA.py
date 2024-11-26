import streamlit as st



# Configurações da página
st.set_page_config(
    page_title="NIXTLA - Forecasting",
    page_icon="🌟",
    layout="wide"
)

st.image(
    "https://th.bing.com/th/id/OIP.6yusAJTcRjlKXiYgw4GxvAHaFj?rs=1&pid=ImgDetMain",
    caption="Making predictive insights accessible to everyone.",
    width=400  # Define a largura em pixels
)

st.markdown('''
# **Bem-vindo à Plataforma de Previsão NIXTLA**
A *Nixtla* é uma empresa de pesquisa e implementação de séries temporais.  
Fornecemos ferramentas de ***previsão de última geração*** que permitem às empresas:  
- Reduzir a **incerteza**  
- Tomar decisões baseadas em dados.
''')

# Linha divisória
st.markdown("---")

# Seção: Método Holt-Winters
st.header("📈 Holt-Winters Method")

st.markdown('''
O ***modelo Holt-Winter***, também conhecido como método de suavização exponencial tripla, é amplamente utilizado em **análise de séries temporais**.  
Ele prevê valores futuros considerando:
- **Tendência**
- **Sazonalidade**

**Vantagens:**  
- Fácil de implementar  
- Requer poucos dados históricos  
- Altamente adaptável  

**Limitações:**  
- Supõe que a sazonalidade seja constante  
- Pode não funcionar bem para séries com mudanças abruptas.
''')

# Linha divisória
st.markdown("---")

# Seção: Previsões Automáticas
st.header("🤖 Automatic Time Series Forecasting")

st.markdown('''
Quando há necessidade de **previsões automáticas** para um grande número de séries temporais (ex.: diferentes produtos ou SKUs), algoritmos automatizados tornam-se essenciais.  

Esses algoritmos:  
- Selecionam modelos de séries temporais apropriados  
- Calculam previsões sem intervenção manual  
- São resistentes a padrões incomuns e aplicáveis em larga escala.
''')

# Linha divisória
st.markdown("---")

# Modelos Automáticos
st.header("🛠️ Modelos Automáticos: Comparação")

st.markdown('''Os modelos **AutoARIMA**, **AutoETS**, **AutoTheta** e **CES** têm diferentes abordagens para modelar séries temporais.  

### 1. **AutoARIMA**  
- **Conceito**: Modela componentes autoregressivos (AR), médias móveis (MA) e integração (I).  
- **Características**: Trabalha bem com séries estacionárias e captura dependências temporais.  
- **Limitações**: Pode não capturar padrões não lineares.

### 2. **AutoETS**  
- **Conceito**: Decomposição da série em erro, tendência e sazonalidade.  
- **Características**: Ideal para séries com sazonalidade clara.  
- **Limitações**: Não modela diretamente relações entre observações passadas.

### 3. **AutoTheta**  
- **Conceito**: Baseado no modelo Theta, que combina tendências lineares e ajustes sazonais.  
- **Características**: Eficaz para tendências de longo prazo e sazonalidade moderada.  
- **Limitações**: Menos eficaz em padrões complexos ou mudanças abruptas.

### 4. **CES (Complex Exponential Smoothing)**  
- **Conceito**: Variante avançada de suavização exponencial, modela séries aditivas e multiplicativas simultaneamente.  
- **Características**: Alta flexibilidade para lidar com mudanças em componentes.  
- **Limitações**: Complexidade computacional maior.
''')

# Linha divisória
st.markdown("---")

# Conclusão
st.markdown('''
### **Conclusão**
Os métodos apresentados oferecem diferentes abordagens para análise e previsão de séries temporais. A escolha do modelo adequado dependerá:  
- Da natureza dos dados (sazonalidade, tendências)  
- Dos objetivos da previsão (curto ou longo prazo).

Explore as ferramentas da *NIXTLA* e maximize o valor das suas séries temporais! 🚀
''')

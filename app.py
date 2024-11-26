import streamlit as st

# Configurações gerais da página
st.set_page_config(
    page_title="Licenciamentos Automóveis",
    page_icon="🚗",
    layout="wide"
)

# Conteúdo principal da página inicial
st.title("Bem-vindo ao Dashboard de Licenciamentos de Automóveis! 🚗")


st.markdown("""
Este dashboard contém:
- **Licenciamentos históricos**: Uma visão detalhada dos licenciamentos desde 1990.
- **Análises detalhadas**: Decomposição sazonal, boxplot e histogramas.
- **Previsões**: Projeções futuras com intervalos de confiança usando modelos estatísticos avançados.

**Dica:** Use o menu lateral para navegar entre as páginas.
""")

# Adicione uma imagem decorativa
st.image(
    "https://cdn.folhape.com.br/img/pc/1100/1/dn_arquivo/2022/01/enquadramento-capa-8_1.jpg",
    caption="licenciamento de automóveis",
    use_column_width=True
)

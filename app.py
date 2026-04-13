import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import init_db
from seed import popular_dados
st.set_page_config(
    page_title="StockFlow — Controle de Estoque & Faturamento",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(, unsafe_allow_html=True)
init_db()
popular_dados()
with st.sidebar:
    st.markdown(, unsafe_allow_html=True)
    st.markdown("###  Navegação")
    pagina = st.radio(
        "Selecione a página",
        options=["Painel Principal", "Produtos", "Estoque",
                 "Caixa", "Relatórios"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown(, unsafe_allow_html=True)
if pagina == "Painel Principal":
    from views.painel import render
    render()
elif pagina == "Produtos":
    from views.produtos import render
    render()
elif pagina == "Estoque":
    from views.estoque import render
    render()
elif pagina == "Caixa":
    from views.caixa import render
    render()
elif pagina == "Relatórios":
    from views.relatorios import render
    render()
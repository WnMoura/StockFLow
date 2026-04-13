import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from services import (
    obter_produtos_mais_vendidos,
    obter_dias_maior_faturamento,
    obter_categorias_maior_giro
)
def formatar_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
def render():
    st.markdown("##  Relatórios")
    st.markdown("---")
    tab1, tab2, tab3 = st.tabs([
        "Produtos Mais Vendidos",
        "Dias com Maior Faturamento",
        "Categorias com Maior Giro"
    ])
    with tab1:
        st.markdown("###  Ranking de Produtos Mais Vendidos")
        dados = obter_produtos_mais_vendidos()
        if dados:
            nomes = [d[0] for d in dados]
            vendas = [int(d[1]) for d in dados]
            fig = go.Figure(go.Bar(
                x=vendas,
                y=nomes,
                orientation="h",
                marker_color=["#4f46e5", "#6366f1", "#818cf8", "#a5b4fc",
                               "#c7d2fe", "#ddd6fe", "#ede9fe", "#f5f3ff",
                               "#faf5ff", "#fdf4ff"][:len(nomes)],
                text=[f"{v} un."for v in vendas],
                textposition="outside",
                textfont=dict(color="#333333", size=12),
            ))
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#333333",
                xaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.1)", title="Unidades Vendidas"),
                yaxis=dict(showgrid=False, autorange="reversed"),
                margin=dict(l=20, r=80, t=10, b=40),
                height=max(300, len(nomes) * 50),
            )
            st.plotly_chart(fig, use_container_width=True)
            df = pd.DataFrame({"Produto": nomes, "Total Vendido": vendas})
            df.index = range(1, len(df) + 1)
            df.index.name = "Posição"
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhuma venda registrada ainda.")
    with tab2:
        st.markdown("###  Dias com Maior Faturamento")
        dados = obter_dias_maior_faturamento()
        if dados:
            from datetime import datetime as dt
            dias = [dt.strptime(str(d[0]), "%Y-%m-%d").strftime("%d/%m/%Y") for d in dados]
            valores = [d[1] for d in dados]
            fig = go.Figure(go.Bar(
                x=dias,
                y=valores,
                marker=dict(
                    color=valores,
                    colorscale=[[0, "#10b981"], [0.5, "#4f46e5"], [1, "#8b5cf6"]],
                ),
                text=[formatar_brl(v) for v in valores],
                textposition="outside",
                textfont=dict(color="#333333", size=11),
            ))
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#333333",
                xaxis=dict(showgrid=False, title="Data"),
                yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.1)", title="Faturamento (R$)"),
                margin=dict(l=20, r=20, t=10, b=40),
                height=400,
            )
            st.plotly_chart(fig, use_container_width=True)
            df = pd.DataFrame({"Data": dias, "Faturamento": [formatar_brl(v) for v in valores]})
            df.index = range(1, len(df) + 1)
            df.index.name = "Posição"
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhum faturamento registrado ainda.")
    with tab3:
        st.markdown("###  Categorias com Maior Giro de Estoque")
        dados = obter_categorias_maior_giro()
        if dados:
            categorias = [d[0] for d in dados]
            totais = [int(d[1]) for d in dados]
            colors_map = {
                "Acessórios": "#4f46e5",
                "Moda Feminina": "#ec4899",
                "Moda Masculina": "#0ea5e9",
                "Moda Fitness": "#10b981",
                "Suplementos": "#f59e0b",
                "Equipamentos": "#8b5cf6",
                "Outros": "#6b7280"
            }
            colors = [colors_map.get(c, "#6b7280") for c in categorias]
            fig = go.Figure(go.Pie(
                labels=categorias,
                values=totais,
                hole=0.5,
                marker=dict(colors=colors),
                textinfo="label+percent",
                textfont=dict(color="white", size=13),
                hovertemplate="<b>%{label}</b><br>Vendas: %{value} un.<br>%{percent}<extra></extra>"
            ))
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#333333",
                showlegend=True,
                legend=dict(font=dict(color="#333333")),
                margin=dict(l=20, r=20, t=10, b=10),
                height=400,
            )
            st.plotly_chart(fig, use_container_width=True)
            df = pd.DataFrame({"Categoria": categorias, "Total Movimentado": totais})
            df.index = range(1, len(df) + 1)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhuma movimentação de venda registrada ainda.")
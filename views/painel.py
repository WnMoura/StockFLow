import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from services import (
    obter_total_estoque, obter_receita_total, obter_despesa_total,
    obter_saldo_caixa, obter_faturamento_ultimos_7_dias,
    obter_evolucao_estoque, obter_produtos_alerta
)
def formatar_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
def render():
    st.markdown("##  Painel Principal")
    st.markdown("---")
    total_estoque = obter_total_estoque()
    receita_total = obter_receita_total()
    despesa_total = obter_despesa_total()
    saldo = obter_saldo_caixa()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon"></div>
            <div class="kpi-value">{total_estoque:,}</div>
            <div class="kpi-label">Unidades em Estoque</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="kpi-card kpi-receita">
            <div class="kpi-icon"></div>
            <div class="kpi-value">{formatar_brl(receita_total)}</div>
            <div class="kpi-label">Receita Total</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="kpi-card kpi-despesa">
            <div class="kpi-icon"></div>
            <div class="kpi-value">{formatar_brl(despesa_total)}</div>
            <div class="kpi-label">Total de Saídas</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        saldo_class = "kpi-negativo"if saldo < 0 else "kpi-positivo"
        st.markdown(f"""
        <div class="kpi-card {saldo_class}">
            <div class="kpi-icon">{'' if saldo < 0 else ''}</div>
            <div class="kpi-value">{formatar_brl(saldo)}</div>
            <div class="kpi-label">Saldo em Caixa</div>
        </div>
        """, unsafe_allow_html=True)
    if saldo < 0:
        st.warning("**Atenção!** O saldo do caixa está negativo. Verifique suas finanças.")
    st.markdown("<br>", unsafe_allow_html=True)
    col_fat, col_est = st.columns(2)
    with col_fat:
        st.markdown("###  Faturamento — Últimos 7 Dias")
        dados_fat = obter_faturamento_ultimos_7_dias()
        if dados_fat:
            hoje = datetime.now().date()
            todos_dias = [(hoje - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]
            fat_dict = {str(d[0]): d[1] for d in dados_fat}
            dias = todos_dias
            valores = [fat_dict.get(d, 0) for d in dias]
            dias_fmt = [datetime.fromisoformat(d).strftime("%d/%m") for d in dias]
            fig = go.Figure(go.Bar(
                x=dias_fmt, y=valores,
                marker_color="#4f46e5",
                marker_line_color="#818cf8",
                marker_line_width=1.5,
                text=[formatar_brl(v) for v in valores],
                textposition="outside",
                textfont=dict(color="#333333", size=11)
            ))
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#333333",
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.1)"),
                margin=dict(l=20, r=20, t=10, b=30),
                height=340,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum faturamento registrado nos últimos 7 dias.")
    with col_est:
        st.markdown("###  Evolução do Estoque")
        dados_est = obter_evolucao_estoque()
        if dados_est:
            df = pd.DataFrame(dados_est, columns=["dia", "tipo", "total"])
            df["dia"] = pd.to_datetime(df["dia"])
            df_pivot = df.pivot_table(index="dia", columns="tipo", values="total", aggfunc="sum").fillna(0)
            if "ENTRADA"not in df_pivot.columns:
                df_pivot["ENTRADA"] = 0
            if "SAÍDA"not in df_pivot.columns:
                df_pivot["SAÍDA"] = 0
            df_pivot["variacao"] = df_pivot.get("ENTRADA", 0) - df_pivot.get("SAÍDA", 0)
            df_pivot["acumulado"] = df_pivot["variacao"].cumsum()
            fig = go.Figure(go.Scatter(
                x=df_pivot.index,
                y=df_pivot["acumulado"],
                mode="lines+markers",
                line=dict(color="#10b981", width=3),
                marker=dict(size=8, color="#34d399"),
                fill="tozeroy",
                fillcolor="rgba(16, 185, 129, 0.1)"
            ))
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#333333",
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.1)"),
                margin=dict(l=20, r=20, t=10, b=30),
                height=340,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhuma movimentação de estoque registrada.")
    st.markdown("###  Alertas de Estoque Baixo")
    alertas = obter_produtos_alerta()
    if alertas:
        for produto in alertas:
            status_class = "badge-esgotado"if produto.quantidade <= 0 else "badge-baixo"
            status_text = "ESGOTADO"if produto.quantidade <= 0 else "BAIXO"
            st.markdown(f"""
            <div class="alert-row">
                <span class="alert-produto">{produto.nome}</span>
                <span class="alert-info">Estoque: <strong>{produto.quantidade}</strong> | Mínimo: <strong>{produto.estoque_minimo}</strong></span>
                <span class="badge {status_class}">{status_text}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("Todos os produtos estão com estoque adequado!")
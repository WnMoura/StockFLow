import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, date
from services import (
    registrar_lancamento, listar_lancamentos,
    obter_receita_total, obter_despesa_total,
    obter_saldo_caixa, obter_despesas_por_categoria,
    zerar_caixa
)
def formatar_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
def render():
    st.markdown("##  Controle de Caixa e Faturamento")
    st.markdown("---")
    receita = obter_receita_total()
    despesa = obter_despesa_total()
    saldo = obter_saldo_caixa()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="kpi-card kpi-receita">
            <div class="kpi-icon"></div>
            <div class="kpi-value">{formatar_brl(receita)}</div>
            <div class="kpi-label">Total de Entradas</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="kpi-card kpi-despesa">
            <div class="kpi-icon"></div>
            <div class="kpi-value">{formatar_brl(despesa)}</div>
            <div class="kpi-label">Total de Saídas</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        s_class = "kpi-negativo"if saldo < 0 else "kpi-positivo"
        st.markdown(f"""
        <div class="kpi-card {s_class}">
            <div class="kpi-icon">{'' if saldo < 0 else ''}</div>
            <div class="kpi-value">{formatar_brl(saldo)}</div>
            <div class="kpi-label">Saldo Final</div>
        </div>
        """, unsafe_allow_html=True)
    if saldo < 0:
        st.warning("**Atenção!** O saldo do caixa está negativo!")
    with st.expander("Resetar Período do Caixa"):
        st.markdown(
            "Use o botão abaixo para **reiniciar os totais do seu caixa** (Entradas, Saídas e Saldo Final).<br>"
            "Isso é útil para começar um novo fechamento do mês ou da semana. "
            "**Fique tranquilo: o Extrato Financeiro não será deletado**, permitindo auditoria no futuro.", 
            unsafe_allow_html=True
        )
        st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
        if st.button("Zerar Totais para Iniciar Novo Período", type="primary", use_container_width=True):
            zerar_caixa()
            st.success("Totais financeiros limpos com sucesso! Extrato mantido.")
            st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    col_grafico, col_form = st.columns([1, 1])
    with col_grafico:
        st.markdown("###  Despesas por Categoria")
        despesas_cat = obter_despesas_por_categoria()
        if despesas_cat:
            categorias = [d[0] for d in despesas_cat]
            valores = [d[1] for d in despesas_cat]
            colors = ["#4f46e5", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4", "#ec4899"]
            fig = go.Figure(go.Pie(
                labels=categorias,
                values=valores,
                hole=0.45,
                marker=dict(colors=colors[:len(categorias)]),
                textinfo="label+percent",
                textfont=dict(color="white", size=12),
                hovertemplate="<b>%{label}</b><br>Valor: R$ %{value:,.2f}<br>%{percent}<extra></extra>"
            ))
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0",
                showlegend=True,
                legend=dict(font=dict(color="#e2e8f0")),
                margin=dict(l=20, r=20, t=10, b=10),
                height=340,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhuma despesa registrada.")
    with col_form:
        st.markdown("###  Novo Lançamento")
        tipo_selecionado = st.selectbox("Tipo de Movimentação *", ["RECEITA", "DESPESA"])
        with st.form("form_lancamento", clear_on_submit=True):
            descricao = st.text_input("Descrição *")
            valor = st.number_input("Valor (R$) *", min_value=0.00, step=0.01, format="%.2f")
            categorias_receita = ["Vendas", "Serviços", "Outros"]
            categorias_despesa = ["Compra de Estoque", "Aluguel", "Utilidades",
                                  "Salários", "Marketing", "Manutenção", "Outros"]
            cats = categorias_receita if tipo_selecionado == "RECEITA"else categorias_despesa
            categoria = st.selectbox("Categoria *", cats)
            data_lanc = st.date_input("Data", value=date.today())
            submitted = st.form_submit_button("Registrar Lançamento", use_container_width=True)
            if submitted:
                if not descricao:
                    st.error("Informe a descrição.")
                else:
                    registrar_lancamento(
                        tipo_selecionado, descricao, valor, categoria,
                        datetime.combine(data_lanc, datetime.min.time())
                    )
                    emoji = ""if tipo_selecionado == "RECEITA"else ""
                    st.success(f"{emoji} Lançamento registrado com sucesso!")
                    st.rerun()
    st.markdown("###  Extrato Financeiro")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        tipo_filtro = st.selectbox("Filtrar por tipo", ["Todos", "RECEITA", "DESPESA"], key="ext_tipo")
    with col_f2:
        data_ini = st.date_input("De", value=date.today().replace(day=1), key="ext_di")
    with col_f3:
        data_fim = st.date_input("Até", value=date.today(), key="ext_df")
    lancamentos = listar_lancamentos(
        tipo=tipo_filtro,
        data_inicio=datetime.combine(data_ini, datetime.min.time()),
        data_fim=datetime.combine(data_fim, datetime.max.time())
    )
    if lancamentos:
        dados = []
        for l in lancamentos:
            dados.append({
                "ID": l.id,
                "Data": l.data.strftime("%d/%m/%Y") if l.data else "",
                "Tipo": l.tipo,
                "Descrição": l.descricao,
                "Categoria": l.categoria,
                "Valor": formatar_brl(l.valor),
            })
        df = pd.DataFrame(dados)
        st.dataframe(df, use_container_width=True, hide_index=True)
        total_periodo_rec = sum(l.valor for l in lancamentos if l.tipo == "RECEITA")
        total_periodo_desp = sum(l.valor for l in lancamentos if l.tipo == "DESPESA")
        saldo_periodo = total_periodo_rec - total_periodo_desp
        st.markdown(f"""
        <div style="display:flex; gap:24px; margin-top:10px;">
            <span style="color:#10b981"> Entradas: <strong>{formatar_brl(total_periodo_rec)}</strong></span>
            <span style="color:#ef4444"> Saídas: <strong>{formatar_brl(total_periodo_desp)}</strong></span>
            <span style="color:{'#10b981' if saldo_periodo >= 0 else '#ef4444'}">
                 Saldo: <strong>{formatar_brl(saldo_periodo)}</strong>
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Nenhum lançamento encontrado no período selecionado.")
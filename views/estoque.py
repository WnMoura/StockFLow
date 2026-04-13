import streamlit as st
import pandas as pd
from datetime import datetime, date
from services import (
    listar_produtos, registrar_entrada, registrar_saida, listar_movimentacoes,
    listar_cores_produto
)
def formatar_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
def render():
    st.markdown("##  Movimentação de Estoque")
    st.markdown("---")
    tab_entrada, tab_saida, tab_hist = st.tabs([
        "Entrada de Mercadoria", "Saída de Mercadoria", "Histórico"
    ])
    produtos = listar_produtos()
    opcoes_produtos = {f"{p.id} — {p.nome}": p.id for p in produtos}
    with tab_entrada:
        st.markdown("### Registrar Entrada de Estoque")
        prod_sel = st.selectbox("Produto *", list(opcoes_produtos.keys()), key="ent_prod")
        produto_id = opcoes_produtos.get(prod_sel)
        cor_selecionada = None
        tamanho_selecionado = None
        cores_prod = listar_cores_produto(produto_id) if produto_id else []
        if cores_prod:
            opcoes_cores = {"(Selecione uma cor)": None}
            for c in cores_prod:
                opcoes_cores[c.nome] = c.id
            col_c, col_t = st.columns(2)
            with col_c:
                nome_cor = st.selectbox("Cor *", list(opcoes_cores.keys()), key="ent_cor")
                cor_selecionada = opcoes_cores[nome_cor]
            with col_t:
                if cor_selecionada is not None:
                    tamanho_selecionado = st.selectbox("Tamanho *", ["Único", "P", "M", "G", "GG"], key="ent_tam")
        with st.form("form_entrada", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                quantidade = st.number_input("Quantidade *", min_value=1, step=1, key="ent_qtd")
                fornecedor = st.text_input("Fornecedor *", key="ent_forn")
            with col2:
                custo_total = st.number_input("Custo Total (R$) *", min_value=0.00, step=0.01, format="%.2f", key="ent_custo")
                data_entrada = st.date_input("Data", value=date.today(), key="ent_data")
            observacao = st.text_area("Observação", key="ent_obs", height=80)
            submitted = st.form_submit_button("Registrar Entrada", use_container_width=True)
            if submitted:
                if not fornecedor:
                    st.error("Informe o fornecedor.")
                elif cores_prod and cor_selecionada is None:
                    st.error("Selecione uma cor e um tamanho para o item.")
                else:
                    try:
                        registrar_entrada(
                            produto_id, quantidade, fornecedor, custo_total,
                            datetime.combine(data_entrada, datetime.min.time()),
                            observacao, cor_selecionada, tamanho_selecionado
                        )
                        st.success(f"Entrada registrada! {quantidade} unidades adicionadas.")
                        st.info(f"Despesa de {formatar_brl(custo_total)} lançada automaticamente no caixa.")
                        st.rerun()
                    except ValueError as e:
                        st.error(str(e))
    with tab_saida:
        st.markdown("### Registrar Saída de Estoque")
        prod_sel_s = st.selectbox("Produto *", list(opcoes_produtos.keys()), key="sai_prod")
        produto_id_s = opcoes_produtos.get(prod_sel_s)
        cor_selecionada_s = None
        tamanho_selecionado_s = None
        cores_prod_s = listar_cores_produto(produto_id_s) if produto_id_s else []
        if cores_prod_s:
            opcoes_cores_s = {"(Selecione uma cor)": None}
            for c in cores_prod_s:
                opcoes_cores_s[c.nome] = c.id
            col_c_s, col_t_s = st.columns(2)
            with col_c_s:
                nome_cor_s = st.selectbox("Cor *", list(opcoes_cores_s.keys()), key="sai_cor")
                cor_selecionada_s = opcoes_cores_s[nome_cor_s]
            with col_t_s:
                if cor_selecionada_s is not None:
                    tamanho_selecionado_s = st.selectbox("Tamanho *", ["Único", "P", "M", "G", "GG"], key="sai_tam")
        with st.form("form_saida", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                quantidade_s = st.number_input("Quantidade *", min_value=1, step=1, key="sai_qtd")
                motivo = st.selectbox("Motivo *", ["venda", "perda", "devolução"], key="sai_mot")
            with col2:
                data_saida = st.date_input("Data", value=date.today(), key="sai_data")
            observacao_s = st.text_area("Observação", key="sai_obs", height=80)
            submitted_s = st.form_submit_button("Registrar Saída", use_container_width=True)
            if submitted_s:
                if cores_prod_s and cor_selecionada_s is None:
                    st.error("Selecione uma cor e um tamanho para o item.")
                else:
                    try:
                        registrar_saida(
                            produto_id_s, quantidade_s, motivo,
                            datetime.combine(data_saida, datetime.min.time()),
                            observacao_s, cor_selecionada_s, tamanho_selecionado_s
                        )
                        st.success(f"Saída registrada! {quantidade_s} unidades removidas.")
                        if motivo == "venda":
                            st.info("Receita de venda lançada automaticamente no caixa.")
                        st.rerun()
                    except ValueError as e:
                        st.error(str(e))
    with tab_hist:
        st.markdown("### Histórico de Movimentações")
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            tipo_filtro = st.selectbox("Tipo", ["Todas", "ENTRADA", "SAÍDA"], key="hist_tipo")
        with col_f2:
            data_ini = st.date_input("De", value=date.today().replace(day=1), key="hist_di")
        with col_f3:
            data_fim = st.date_input("Até", value=date.today(), key="hist_df")
        movs = listar_movimentacoes(
            tipo=tipo_filtro,
            data_inicio=datetime.combine(data_ini, datetime.min.time()),
            data_fim=datetime.combine(data_fim, datetime.max.time())
        )
        if movs:
            dados = []
            for m in movs:
                dados.append({
                    "ID": m.id,
                    "Data": m.data.strftime("%d/%m/%Y %H:%M") if m.data else "",
                    "Produto": m.produto.nome if m.produto else "—",
                    "Tipo": m.tipo,
                    "Quantidade": m.quantidade,
                    "Motivo": m.motivo or "—",
                    "Fornecedor": m.fornecedor or "—",
                    "Custo Total": formatar_brl(m.custo_total) if m.custo_total else "—",
                })
            df = pd.DataFrame(dados)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"Total de registros: {len(dados)}")
        else:
            st.info("Nenhuma movimentação encontrada no período selecionado.")
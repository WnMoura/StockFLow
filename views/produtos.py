import streamlit as st
import streamlit.components.v1 as components
from services import (
    criar_produto, listar_produtos, atualizar_produto,
    excluir_produto, listar_categorias,
    adicionar_cor, listar_cores_produto, remover_cor, atualizar_cor_quantidade,
    listar_todas_cores_unicas
)
def formatar_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
CORES_PREDEFINIDAS = {
    "Preto": "#1a1a1a", "Branco": "#f5f5f5", "Cinza": "#6b7280", "Cinza Escuro": "#374151",
    "Vermelho": "#dc2626", "Rosa": "#e91e8c", "Vinho": "#7c2d3e", "Azul": "#2563eb",
    "Azul Marinho": "#1e3a5f", "Azul Royal": "#2563eb", "Verde": "#16a34a",
    "Verde Militar": "#4a5d23", "Amarelo": "#eab308", "Laranja": "#ea580c",
    "Roxo": "#7c3aed", "Bege": "#d4a574", "Inox": "#c0c0c0", "Personalizada": None,
}
def render():
    try:
        CORES_PREDEFINIDAS.update(listar_todas_cores_unicas())
    except Exception:
        pass
    st.markdown("##  Gestão de Produtos")
    st.markdown("---")
    tab_lista, tab_cadastro = st.tabs(["Lista de Produtos", "Cadastrar Novo Produto"])
    with tab_cadastro:
        st.markdown("### Cadastrar Novo Produto")
        st.markdown("####  Informações Básicas")
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome do Produto *", key="cad_nome")
            categorias_cad = ["Moda Feminina", "Moda Masculina", "Acessórios",
                              "Calçados", "Suplementos", "Outros"]
            categoria = st.selectbox("Categoria *", categorias_cad, key="cad_cat")
            valor_compra = st.number_input("Valor de Compra (R$) *", min_value=0.00, step=0.01, format="%.2f", key="cad_vcompra")
            custos_variaveis = st.number_input("Custos Variáveis (Frete, Brindes) (R$)", min_value=0.00, step=0.01, format="%.2f", key="cad_cvar")
            preco_custo = valor_compra + custos_variaveis
            st.markdown(f"<div style='margin-top:14px;'><span style='color:#cbd5e1;font-size:0.85rem'>Preço de Custo Final:</span><br><b>R$ {preco_custo:.2f}</b></div>", unsafe_allow_html=True)
        with col2:
            preco_venda = st.number_input("Preço de Venda (R$) *", min_value=0.00, step=0.01, format="%.2f", key="cad_venda")
            estoque_minimo = st.number_input("Estoque Mínimo *", min_value=0, step=1, value=5, key="cad_min")
        st.markdown("<br><hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        st.markdown("####  Definir Cores e Tamanhos (Opcional)")
        st.markdown("**Selecione cores pré-definidas e cadastre o estoque inicial de cada tamanho:**")
        cores_selecionadas = st.multiselect(
            "Selecione cores pré-definidas",
            [c for c in CORES_PREDEFINIDAS.keys() if c != "Personalizada"],
            key="cores_predefinidas"
        )
        cor_dados = {}
        if cores_selecionadas:
            st.markdown("<br>", unsafe_allow_html=True)
        for cnome in cores_selecionadas:
            st.markdown(f"**{cnome}**")
            p, m, g, gg, u = st.columns(5)
            vp = p.number_input("P", min_value=0, key=f"c_p_{cnome}", step=1)
            vm = m.number_input("M", min_value=0, key=f"c_m_{cnome}", step=1)
            vg = g.number_input("G", min_value=0, key=f"c_g_{cnome}", step=1)
            vgg = gg.number_input("GG", min_value=0, key=f"c_gg_{cnome}", step=1)
            vu = u.number_input("Único", min_value=0, key=f"c_u_{cnome}", step=1)
            cor_dados[cnome] = {"p": vp, "m": vm, "g": vg, "gg": vgg, "u": vu, "hex": CORES_PREDEFINIDAS[cnome]}
        st.markdown("**Cor personalizada (Caso não tenha achado na lista acima)**")
        col_p1, col_p2 = st.columns([3, 1])
        with col_p1:
            nome_cor_pers = st.text_input("Nome da Cor Personalizada", key="nome_cor_pers")
        with col_p2:
            st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
            hex_cor_pers = st.color_picker("Cor", value="#6366f1", key="hex_cor_pers_cad", label_visibility="collapsed")
        p_p, p_m, p_g, p_gg, p_u = st.columns(5)
        vp_p = p_p.number_input("P", min_value=0, key="c_p_pers", step=1)
        vm_p = p_m.number_input("M", min_value=0, key="c_m_pers", step=1)
        vg_p = p_g.number_input("G", min_value=0, key="c_g_pers", step=1)
        vgg_p = p_gg.number_input("GG", min_value=0, key="c_gg_pers", step=1)
        vu_p = p_u.number_input("Único", min_value=0, key="c_u_pers", step=1)
        if nome_cor_pers.strip():
            cor_dados[nome_cor_pers.strip()] = {"p": vp_p, "m": vm_p, "g": vg_p, "gg": vgg_p, "u": vu_p, "hex": hex_cor_pers}
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.button("Cadastrar Produto", type="primary", use_container_width=True) 
        if submitted:
            if not nome:
                st.error("O nome do produto é obrigatório.")
            else:
                if preco_venda <= preco_custo:
                    st.warning("O preço de venda é menor ou igual ao custo!")
                novo_prod = criar_produto(nome, categoria, preco_custo, preco_venda, 0, estoque_minimo, valor_compra, custos_variaveis)
                for cnome, data in cor_dados.items():
                    total = data["p"] + data["m"] + data["g"] + data["gg"] + data["u"]
                    adicionar_cor(novo_prod.id, cnome, data["hex"], quantidade=total, qtd_p=data["p"], qtd_m=data["m"], qtd_g=data["g"], qtd_gg=data["gg"])
                st.success(f"Produto '{nome}' cadastrado com sucesso!")
    with tab_lista:
        st.markdown("###  Lista de Produtos")
        col_filtro1, col_filtro2 = st.columns([1, 2])
        with col_filtro1:
            categorias = ["Todas"] + listar_categorias()
            cat_filtro = st.selectbox("Filtrar por Categoria", categorias, key="filtro_cat")
        with col_filtro2:
            busca = st.text_input("Buscar por nome", key="busca_produto")
        produtos = listar_produtos(
            categoria=cat_filtro if cat_filtro != "Todas"else None,
            busca=busca if busca else None
        )
        if not produtos:
            st.info("Nenhum produto encontrado.")
        else:
            st.markdown(, unsafe_allow_html=True)
            for prod in produtos:
                badge_map = {
                    "OK": ("badge-ok", "OK"),
                    "BAIXO": ("badge-baixo", "BAIXO"),
                    "ESGOTADO": ("badge-esgotado", "ESGOTADO"),
                }
                badge_class, badge_text = badge_map.get(prod.status, ("badge-ok", "OK"))
                cores_prod = listar_cores_produto(prod.id)
                col_id, col_nome, col_cat, col_venda, col_compra, col_cvar, col_lucro, col_est, col_status, col_cores, col_acoes = st.columns(
                    [0.8, 2.6, 1.8, 1.6, 1.6, 1.6, 1.6, 1.2, 1.6, 3.6, 2.0]
                )
                with col_id:
                    st.markdown(f"<span class='mobile-label'>ID</span> **{prod.id}**", unsafe_allow_html=True)
                with col_nome:
                    st.markdown(f"<span class='mobile-label'>Nome</span> {prod.nome}", unsafe_allow_html=True)
                with col_cat:
                    st.markdown(f"<span class='mobile-label'>Categoria</span> `{prod.categoria}`", unsafe_allow_html=True)
                with col_venda:
                    st.markdown(f"<span class='mobile-label'>Venda</span> <b style='color:#a3e635;font-size:0.85rem'>{formatar_brl(prod.preco_venda)}</b>", unsafe_allow_html=True)
                with col_compra:
                    st.markdown(f"<span class='mobile-label'>Compra</span> <span style='font-size:0.85rem'>{formatar_brl(prod.valor_compra)}</span>", unsafe_allow_html=True)
                with col_cvar:
                    st.markdown(f"<span class='mobile-label'>C. Var</span> <span style='font-size:0.85rem'>{formatar_brl(prod.custos_variaveis)}</span>", unsafe_allow_html=True)
                with col_lucro:
                    lucro = prod.preco_venda - (prod.valor_compra + prod.custos_variaveis)
                    lucro_color = "#a3e635"if lucro >= 0 else "#ef4444"
                    st.markdown(f"<span class='mobile-label'>Lucro</span> <b style='color:{lucro_color};font-size:0.85rem'>{formatar_brl(lucro)}</b>", unsafe_allow_html=True)
                with col_est:
                    st.markdown(f"<span class='mobile-label'>Estoque</span> **{prod.quantidade}**", unsafe_allow_html=True)
                with col_status:
                    st.markdown(f'<div style="display:flex; justify-content:center; align-items:center;"><span class="mobile-label">Status</span> <span class="badge {badge_class}">{badge_text}</span></div>', unsafe_allow_html=True)
                with col_cores:
                    cores_html = ""
                    if cores_prod:
                        circles = '<div style="display:flex; flex-wrap:wrap; gap:8px;">'
                        for c in cores_prod:
                            border = "2px solid rgba(255,255,255,0.3)"if c.hex_cor.lower() in ("#f5f5f5", "#ffffff") else "2px solid rgba(255,255,255,0.1)"
                            tamanhos = []
                            if getattr(c, 'qtd_p', 0) > 0: tamanhos.append("P")
                            if getattr(c, 'qtd_m', 0) > 0: tamanhos.append("M")
                            if getattr(c, 'qtd_g', 0) > 0: tamanhos.append("G")
                            if getattr(c, 'qtd_gg', 0) > 0: tamanhos.append("GG")
                            unico = c.quantidade - (getattr(c, 'qtd_p', 0) + getattr(c, 'qtd_m', 0) + getattr(c, 'qtd_g', 0) + getattr(c, 'qtd_gg', 0))
                            if unico > 0: tamanhos.append("U")
                            tamanhos_str = ",".join(tamanhos) if tamanhos else "-"
                            circles += (
                                f'<div style="display:flex; flex-direction:column; align-items:center; gap:2px;"title="{c.nome} (Total: {c.quantidade} | P:{getattr(c, "qtd_p", 0)} M:{getattr(c, "qtd_m", 0)} G:{getattr(c, "qtd_g", 0)} GG:{getattr(c, "qtd_gg", 0)})">'
                                f'  <div style="display:flex; align-items:center; gap:4px; background:rgba(255,255,255,0.05); padding:2px 6px; border-radius:12px;">'
                                f'    <span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:{c.hex_cor};border:{border};"></span>'
                                f'    <span style="font-size:0.75rem;color:#cbd5e1;font-weight:bold;">{c.quantidade}</span>'
                                f'  </div>'
                                f'  <span style="font-size:0.55rem;color:#94a3b8;line-height:1;margin-top:-2px;">{tamanhos_str}</span>'
                                f'</div>'
                            )
                        circles += '</div>'
                        cores_html = circles
                    else:
                        cores_html = '<span style="color:#64748b;font-size:0.8rem;">Sem cores</span>'
                    st.markdown(f"<div style='display:flex; justify-content:center; align-items:center;'><span class='mobile-label'>Cores</span> {cores_html}</div>", unsafe_allow_html=True)
                with col_acoes:
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if st.button("✏️", key=f"edit_{prod.id}", help="Editar Informações & Cores", use_container_width=True):
                            st.session_state[f"editing_{prod.id}"] = not st.session_state.get(f"editing_{prod.id}", False)
                    with btn_col2:
                        if st.button("❌", key=f"del_{prod.id}", help="Excluir", use_container_width=True):
                            excluir_produto(prod.id)
                            st.success(f"Produto '{prod.nome}' removido.")
                            st.rerun()
                if st.session_state.get(f"editing_{prod.id}", False):
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(30,41,59,0.8), rgba(15,23,42,0.9));
                                border: 1px solid rgba(148,163,184,0.3); border-radius: 14px;
                                padding: 20px; margin: 8px 0 16px;">
                        <span style="font-size:1.1rem; font-weight:600; color:#f8fafc; margin-bottom: 20px; display:inline-block;">
                             Modo de Edição Completo - {prod.nome}
                        </span>
                    """, unsafe_allow_html=True)
                    st.markdown("####  Detalhes e Valores")
                    ec1, ec2 = st.columns(2)
                    categorias_edit = ["Moda Feminina", "Moda Masculina", "Acessórios",
                                       "Calçados", "Suplementos", "Outros"]
                    with ec1:
                        novo_nome = st.text_input("Nome", value=prod.nome, key=f"nome_{prod.id}")
                        nova_cat = st.selectbox("Categoria", categorias_edit,
                            index=categorias_edit.index(prod.categoria) if prod.categoria in categorias_edit else len(categorias_edit) - 1, key=f"cat_{prod.id}")
                        novo_valor_compra = st.number_input("Valor Compra", value=prod.valor_compra, format="%.2f", min_value=0.00, step=0.01, key=f"vc_{prod.id}")
                        novo_custos = st.number_input("Custos Var.", value=prod.custos_variaveis, format="%.2f", min_value=0.00, step=0.01, key=f"cv_{prod.id}")
                        novo_custo = novo_valor_compra + novo_custos
                    with ec2:
                        novo_preco = st.number_input("Preço Venda", value=prod.preco_venda, format="%.2f", min_value=0.00, step=0.01, key=f"pv_{prod.id}")
                        if cores_prod:
                            st.markdown(f"<div style='margin-bottom:8px;'><span style='font-size:0.85rem;color:#cbd5e1;'>Quantidade (Bloqueado, some nas cores)</span><br><b>{prod.quantidade}</b></div>", unsafe_allow_html=True)
                            nova_qtd = prod.quantidade
                        else:
                            nova_qtd = st.number_input("Quantidade Inicial", value=prod.quantidade, min_value=0, key=f"qi_{prod.id}")
                        novo_min = st.number_input("Estoque Mínimo", value=prod.estoque_minimo, min_value=0, key=f"em_{prod.id}")
                    st.markdown("---")
                    st.markdown("####  Central de Cores e Tamanhos")
                    cores_atuais = listar_cores_produto(prod.id)
                    tab_manage, tab_add = st.tabs(["Alterar Estoque da Grade", "Adicionar Nova Cor à Grade"])
                    with tab_manage:
                        if cores_atuais:
                            cols_cores = st.columns(3)
                            for idx, cor in enumerate(cores_atuais):
                                col_idx = idx % 3
                                with cols_cores[col_idx]:
                                    border_style = "2px solid rgba(255,255,255,0.4)"if cor.hex_cor.lower() in ("#f5f5f5", "#ffffff") else "none"
                                    st.markdown(f"""
                                    <div style="background: rgba(15,23,42,0.5); border: 1px solid rgba(79,70,229,0.3);
                                                border-radius: 8px; padding: 10px; margin-bottom: 6px;">
                                        <div style="display:flex; align-items:center; gap:8px; margin-bottom: 8px;">
                                            <div style="width:20px; height:20px; border-radius:50%; background:{cor.hex_cor};
                                                        border:{border_style}; box-shadow: 0 2px 8px {cor.hex_cor}40;"></div>
                                            <span style="color:#e2e8f0; font-size:0.9rem; font-weight:600;">{cor.nome}</span>
                                        </div>
                                    """, unsafe_allow_html=True)
                                    s_p, s_m, s_g, s_gg = st.columns(4)
                                    with s_p: np = st.number_input("P", value=cor.qtd_p, min_value=0, step=1, key=f"p_{cor.id}")
                                    with s_m: nm = st.number_input("M", value=cor.qtd_m, min_value=0, step=1, key=f"m_{cor.id}")
                                    with s_g: ng = st.number_input("G", value=cor.qtd_g, min_value=0, step=1, key=f"g_{cor.id}")
                                    with s_gg: ngg = st.number_input("GG", value=cor.qtd_gg, min_value=0, step=1, key=f"gg_{cor.id}")
                                    s_u, s_btn = st.columns([2, 1])
                                    with s_u:
                                        unico = cor.quantidade - (cor.qtd_p+cor.qtd_m+cor.qtd_g+cor.qtd_gg)
                                        nu = st.number_input("Tamanho Único", value=max(0, unico), min_value=0, step=1, key=f"u_{cor.id}")
                                    with s_btn:
                                        st.markdown("<div style='margin-top:28px'></div>", unsafe_allow_html=True)
                                        if st.button("❌", key=f"rmcor_{cor.id}", help="Remover"):
                                            remover_cor(cor.id)
                                            st.rerun()
                                    new_total = np + nm + ng + ngg + nu
                                    if np != cor.qtd_p or nm != cor.qtd_m or ng != cor.qtd_g or ngg != cor.qtd_gg or new_total != cor.quantidade:
                                        atualizar_cor_quantidade(cor.id, new_total, np, nm, ng, ngg)
                                        st.rerun()
                                    st.markdown("</div>", unsafe_allow_html=True)
                        else:
                            st.info("Nenhuma cor cadastrada ainda. Adicione uma nova cor ao lado.")
                    with tab_add:
                        with st.container():
                            st.markdown("**Selecione a cor e aloque a quantidade**")
                            fc1, fc2, fc_qtd, fc3 = st.columns([2, 1.5, 1, 1])
                            with fc1:
                                cor_selecionada = st.selectbox("Cor", list(CORES_PREDEFINIDAS.keys()), key=f"sel_cor_{prod.id}")
                            with fc2:
                                if cor_selecionada == "Personalizada":
                                    nome_cor = st.text_input("Nome", key=f"npers_cor_{prod.id}")
                                    st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
                                    hex_val = st.color_picker("Cor", value="#6366f1", key=f"hpers_cor_{prod.id}", label_visibility="collapsed")
                                else:
                                    nome_cor = cor_selecionada
                                    hex_val = CORES_PREDEFINIDAS.get(cor_selecionada, "#000000")
                                    st.markdown(f"""
                                    <div style="display:flex; align-items:center; gap:8px; padding:10px 0;">
                                        <div style="width:24px;height:24px;border-radius:50%;background:{hex_val};border:2px solid rgba(255,255,255,0.2);"></div>
                                        <span style="color:#94a3b8; font-size:0.85rem;">{hex_val}</span>
                                    </div>
                                    """, unsafe_allow_html=True)
                            with fc_qtd:
                                qtd_nova_cor = st.number_input("Qtd", min_value=0, step=1, value=0, key=f"qtd_nova_{prod.id}")
                            with fc3:
                                st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
                                add_cor = st.button("Salvar", key=f"btn_add_cor_{prod.id}", use_container_width=True)
                            if add_cor:
                                if cor_selecionada == "Personalizada"and not nome_cor:
                                    st.error("Informe um nome para a cor personalizada.")
                                else:
                                    cores_existentes = [c.nome.lower() for c in cores_atuais] if cores_atuais else []
                                    if nome_cor.lower() in cores_existentes:
                                        st.warning(f"A cor '{nome_cor}' já existe!")
                                    else:
                                        remover_cor(0) 
                                        adicionar_cor(prod.id, nome_cor, hex_val, qtd_nova_cor)
                                        st.success(f"Adicionada!")
                                        st.rerun()
                    st.markdown("---")
                    bcol1, bcol2 = st.columns(2)
                    with bcol1:
                        if st.button("Salvar Alterações Básicas", key=f"save_{prod.id}", type="primary", use_container_width=True):
                            atualizar_produto(prod.id, nome=novo_nome, categoria=nova_cat,
                                              preco_custo=novo_custo, preco_venda=novo_preco,
                                              valor_compra=novo_valor_compra, custos_variaveis=novo_custos,
                                              quantidade=nova_qtd, estoque_minimo=novo_min)
                            st.success(f"Alterações no produto '{novo_nome}' foram salvas!")
                            st.rerun()
                    with bcol2:
                        if st.button("Fechar Modo Edição", key=f"cancel_{prod.id}", use_container_width=True):
                            st.session_state[f"editing_{prod.id}"] = False
                            st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True) 
                st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 2px 0;'>", unsafe_allow_html=True)
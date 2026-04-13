from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from models import Produto, MovimentacaoEstoque, LancamentoFinanceiro, CorProduto
from datetime import datetime, timedelta
from database import get_session
def criar_produto(nome: str, categoria: str, preco_custo: float,
                  preco_venda: float, quantidade: int, estoque_minimo: int,
                  valor_compra: float = 0.0, custos_variaveis: float = 0.0) -> Produto:
    session = get_session()
    try:
        produto = Produto(
            nome=nome, categoria=categoria,
            preco_custo=preco_custo, preco_venda=preco_venda,
            quantidade=quantidade, estoque_minimo=estoque_minimo,
            valor_compra=valor_compra, custos_variaveis=custos_variaveis
        )
        session.add(produto)
        session.commit()
        session.refresh(produto)
        return produto
    finally:
        session.close()
def listar_produtos(apenas_ativos=True, categoria=None, busca=None):
    session = get_session()
    try:
        query = session.query(Produto)
        if apenas_ativos:
            query = query.filter(Produto.ativo == True)  
        if categoria and categoria != "Todas":
            query = query.filter(Produto.categoria == categoria)
        if busca:
            query = query.filter(Produto.nome.ilike(f"%{busca}%"))
        return query.order_by(Produto.nome).all()
    finally:
        session.close()
def obter_produto(produto_id: int):
    session = get_session()
    try:
        return session.query(Produto).filter(Produto.id == produto_id).first()
    finally:
        session.close()
def atualizar_produto(produto_id: int, **kwargs):
    session = get_session()
    try:
        produto = session.query(Produto).filter(Produto.id == produto_id).first()
        if produto:
            for k, v in kwargs.items():
                setattr(produto, k, v)
            produto.atualizado_em = datetime.now()
            session.commit()
            session.refresh(produto)
        return produto
    finally:
        session.close()
def excluir_produto(produto_id: int):
    session = get_session()
    try:
        produto = session.query(Produto).filter(Produto.id == produto_id).first()
        if produto:
            produto.ativo = False
            produto.atualizado_em = datetime.now()
            session.commit()
    finally:
        session.close()
def listar_categorias():
    session = get_session()
    try:
        cats = session.query(Produto.categoria).filter(Produto.ativo == True).distinct().all()  
        return sorted([c[0] for c in cats])
    finally:
        session.close()
def adicionar_cor(produto_id: int, nome: str, hex_cor: str, quantidade: int = 0, qtd_p: int = 0, qtd_m: int = 0, qtd_g: int = 0, qtd_gg: int = 0) -> CorProduto:
    session = get_session()
    try:
        cor = CorProduto(produto_id=produto_id, nome=nome, hex_cor=hex_cor, quantidade=quantidade, qtd_p=qtd_p, qtd_m=qtd_m, qtd_g=qtd_g, qtd_gg=qtd_gg)
        session.add(cor)
        session.commit()
        session.refresh(cor)
        _sync_produto_quantidade(session, produto_id)
        session.commit()
        return cor
    finally:
        session.close()
def listar_cores_produto(produto_id: int):
    session = get_session()
    try:
        return session.query(CorProduto).filter(
            CorProduto.produto_id == produto_id
        ).order_by(CorProduto.nome).all()
    finally:
        session.close()
def remover_cor(cor_id: int):
    session = get_session()
    try:
        cor = session.query(CorProduto).filter(CorProduto.id == cor_id).first()
        if cor:
            produto_id = cor.produto_id
            session.delete(cor)
            session.commit()
            _sync_produto_quantidade(session, produto_id)
            session.commit()
    finally:
        session.close()
def atualizar_cor(cor_id: int, nome: str, hex_cor: str):
    session = get_session()
    try:
        cor = session.query(CorProduto).filter(CorProduto.id == cor_id).first()
        if cor:
            cor.nome = nome
            cor.hex_cor = hex_cor
            session.commit()
    finally:
        session.close()
def atualizar_cor_quantidade(cor_id: int, quantidade: int, qtd_p: int = 0, qtd_m: int = 0, qtd_g: int = 0, qtd_gg: int = 0):
    session = get_session()
    try:
        cor = session.query(CorProduto).filter(CorProduto.id == cor_id).first()
        if cor:
            cor.quantidade = quantidade
            cor.qtd_p = qtd_p
            cor.qtd_m = qtd_m
            cor.qtd_g = qtd_g
            cor.qtd_gg = qtd_gg
            session.commit()
            _sync_produto_quantidade(session, cor.produto_id)
            session.commit()
    finally:
        session.close()
def _sync_produto_quantidade(session, produto_id: int):
    produto = session.query(Produto).filter(Produto.id == produto_id).first()
    if produto:
        cores = session.query(CorProduto).filter(CorProduto.produto_id == produto_id).all()
        if cores:
            produto.quantidade = sum(c.quantidade for c in cores)
def registrar_entrada(produto_id: int, quantidade: int, fornecedor: str,
                      custo_total: float, data: datetime = None, observacao: str = "",
                      cor_id: int = None, tamanho: str = None):
    session = get_session()
    try:
        produto = session.query(Produto).filter(Produto.id == produto_id).first()
        if not produto:
            raise ValueError("Produto não encontrado.")
        if cor_id:
            cor = session.query(CorProduto).filter(CorProduto.id == cor_id).first()
            if not cor:
                raise ValueError("Cor não encontrada.")
            if tamanho == "P": cor.qtd_p += quantidade
            elif tamanho == "M": cor.qtd_m += quantidade
            elif tamanho == "G": cor.qtd_g += quantidade
            elif tamanho == "GG": cor.qtd_gg += quantidade
            cor.quantidade += quantidade
            session.commit()
            _sync_produto_quantidade(session, produto_id)
        else:
            produto.quantidade += quantidade
        mov = MovimentacaoEstoque(
            produto_id=produto_id, cor_id=cor_id, tamanho=tamanho, tipo="ENTRADA", quantidade=quantidade,
            motivo="reposição", fornecedor=fornecedor,
            custo_total=custo_total, data=data or datetime.now(),
            observacao=observacao
        )
        session.add(mov)
        produto.atualizado_em = datetime.now()
        lancamento = LancamentoFinanceiro(
            tipo="DESPESA",
            descricao=f"Compra de estoque: {produto.nome} ({quantidade} un.)",
            valor=custo_total,
            categoria="Compra de Estoque",
            data=data or datetime.now()
        )
        session.add(lancamento)
        session.commit()
        return mov
    finally:
        session.close()
def registrar_saida(produto_id: int, quantidade: int, motivo: str,
                    data: datetime = None, observacao: str = "",
                    cor_id: int = None, tamanho: str = None):
    session = get_session()
    try:
        produto = session.query(Produto).filter(Produto.id == produto_id).first()
        if not produto:
            raise ValueError("Produto não encontrado.")
        if cor_id:
            cor = session.query(CorProduto).filter(CorProduto.id == cor_id).first()
            if not cor:
                raise ValueError("Cor não encontrada.")
            unico = cor.quantidade - (cor.qtd_p + cor.qtd_m + cor.qtd_g + cor.qtd_gg)
            if tamanho == "P"and cor.qtd_p < quantidade: raise ValueError("Estoque insuficiente de P.")
            elif tamanho == "M"and cor.qtd_m < quantidade: raise ValueError("Estoque insuficiente de M.")
            elif tamanho == "G"and cor.qtd_g < quantidade: raise ValueError("Estoque insuficiente de G.")
            elif tamanho == "GG"and cor.qtd_gg < quantidade: raise ValueError("Estoque insuficiente de GG.")
            elif tamanho == "Único"and unico < quantidade: raise ValueError("Estoque insuficiente de Tamanho único.")
            if tamanho == "P": cor.qtd_p -= quantidade
            elif tamanho == "M": cor.qtd_m -= quantidade
            elif tamanho == "G": cor.qtd_g -= quantidade
            elif tamanho == "GG": cor.qtd_gg -= quantidade
            cor.quantidade -= quantidade
            session.commit()
            _sync_produto_quantidade(session, produto_id)
        else:
            if produto.quantidade < quantidade:
                raise ValueError(f"Estoque insuficiente. Disponível: {produto.quantidade}")
            produto.quantidade -= quantidade
        mov = MovimentacaoEstoque(
            produto_id=produto_id, cor_id=cor_id, tamanho=tamanho, tipo="SAÍDA", quantidade=quantidade,
            motivo=motivo, data=data or datetime.now(),
            observacao=observacao
        )
        session.add(mov)
        produto.atualizado_em = datetime.now()
        if motivo == "venda":
            receita = LancamentoFinanceiro(
                tipo="RECEITA",
                descricao=f"Venda: {produto.nome} ({quantidade} un.)",
                valor=produto.preco_venda * quantidade,
                categoria="Vendas",
                data=data or datetime.now()
            )
            session.add(receita)
        session.commit()
        return mov
    finally:
        session.close()
def listar_movimentacoes(tipo=None, data_inicio=None, data_fim=None):
    session = get_session()
    try:
        query = session.query(MovimentacaoEstoque).options(
            joinedload(MovimentacaoEstoque.produto)
        )
        if tipo and tipo != "Todas":
            query = query.filter(MovimentacaoEstoque.tipo == tipo)
        if data_inicio:
            query = query.filter(MovimentacaoEstoque.data >= data_inicio)
        if data_fim:
            query = query.filter(MovimentacaoEstoque.data <= data_fim)
        results = query.order_by(desc(MovimentacaoEstoque.data)).all()
        for r in results:
            _ = r.produto.nome if r.produto else None
        return results
    finally:
        session.close()
def registrar_lancamento(tipo: str, descricao: str, valor: float,
                         categoria: str, data: datetime = None, observacao: str = ""):
    session = get_session()
    try:
        lancamento = LancamentoFinanceiro(
            tipo=tipo, descricao=descricao, valor=valor,
            categoria=categoria, data=data or datetime.now(),
            observacao=observacao
        )
        session.add(lancamento)
        session.commit()
        session.refresh(lancamento)
        return lancamento
    finally:
        session.close()
def listar_lancamentos(tipo=None, data_inicio=None, data_fim=None):
    session = get_session()
    try:
        query = session.query(LancamentoFinanceiro)
        if tipo and tipo != "Todos":
            query = query.filter(LancamentoFinanceiro.tipo == tipo)
        if data_inicio:
            query = query.filter(LancamentoFinanceiro.data >= data_inicio)
        if data_fim:
            query = query.filter(LancamentoFinanceiro.data <= data_fim)
        return query.order_by(desc(LancamentoFinanceiro.data)).all()
    finally:
        session.close()
def zerar_caixa():
    session = get_session()
    try:
        session.query(LancamentoFinanceiro).filter(
            LancamentoFinanceiro.arquivado == False
        ).update({LancamentoFinanceiro.arquivado: True})
        session.commit()
    finally:
        session.close()
def obter_total_estoque():
    session = get_session()
    try:
        total = session.query(func.sum(Produto.quantidade)).filter(
            Produto.ativo == True  
        ).scalar()
        return total or 0
    finally:
        session.close()
def obter_receita_total():
    session = get_session()
    try:
        total = session.query(func.sum(LancamentoFinanceiro.valor)).filter(
            LancamentoFinanceiro.tipo == "RECEITA",
            LancamentoFinanceiro.arquivado == False
        ).scalar()
        return total or 0.0
    finally:
        session.close()
def obter_despesa_total():
    session = get_session()
    try:
        total = session.query(func.sum(LancamentoFinanceiro.valor)).filter(
            LancamentoFinanceiro.tipo == "DESPESA",
            LancamentoFinanceiro.arquivado == False
        ).scalar()
        return total or 0.0
    finally:
        session.close()
def obter_saldo_caixa():
    return obter_receita_total() - obter_despesa_total()
def obter_faturamento_ultimos_7_dias():
    session = get_session()
    try:
        data_limite = datetime.now() - timedelta(days=7)
        lancamentos = session.query(
            func.date(LancamentoFinanceiro.data).label("dia"),
            func.sum(LancamentoFinanceiro.valor).label("total")
        ).filter(
            LancamentoFinanceiro.tipo == "RECEITA",
            LancamentoFinanceiro.arquivado == False,
            LancamentoFinanceiro.data >= data_limite
        ).group_by(func.date(LancamentoFinanceiro.data)).all()
        return lancamentos
    finally:
        session.close()
def obter_evolucao_estoque():
    session = get_session()
    try:
        movs = session.query(
            func.date(MovimentacaoEstoque.data).label("dia"),
            MovimentacaoEstoque.tipo,
            func.sum(MovimentacaoEstoque.quantidade).label("total")
        ).group_by(
            func.date(MovimentacaoEstoque.data), MovimentacaoEstoque.tipo
        ).order_by(func.date(MovimentacaoEstoque.data)).all()
        return movs
    finally:
        session.close()
def obter_produtos_alerta():
    session = get_session()
    try:
        produtos = session.query(Produto).filter(
            Produto.ativo == True,  
            Produto.quantidade <= Produto.estoque_minimo
        ).order_by(Produto.quantidade).all()
        return produtos
    finally:
        session.close()
def obter_produtos_mais_vendidos(limite=10):
    session = get_session()
    try:
        resultados = session.query(
            Produto.nome,
            func.sum(MovimentacaoEstoque.quantidade).label("total_vendido")
        ).join(MovimentacaoEstoque).filter(
            MovimentacaoEstoque.motivo == "venda"
        ).group_by(Produto.nome).order_by(
            desc("total_vendido")
        ).limit(limite).all()
        return resultados
    finally:
        session.close()
def obter_dias_maior_faturamento(limite=10):
    session = get_session()
    try:
        resultados = session.query(
            func.date(LancamentoFinanceiro.data).label("dia"),
            func.sum(LancamentoFinanceiro.valor).label("total")
        ).filter(
            LancamentoFinanceiro.tipo == "RECEITA",
            LancamentoFinanceiro.arquivado == False
        ).group_by(
            func.date(LancamentoFinanceiro.data)
        ).order_by(desc("total")).limit(limite).all()
        return resultados
    finally:
        session.close()
def obter_categorias_maior_giro():
    session = get_session()
    try:
        resultados = session.query(
            Produto.categoria,
            func.sum(MovimentacaoEstoque.quantidade).label("total_movimentado")
        ).join(MovimentacaoEstoque).filter(
            MovimentacaoEstoque.motivo == "venda"
        ).group_by(Produto.categoria).order_by(
            desc("total_movimentado")
        ).all()
        return resultados
    finally:
        session.close()
def obter_despesas_por_categoria():
    session = get_session()
    try:
        resultados = session.query(
            LancamentoFinanceiro.categoria,
            func.sum(LancamentoFinanceiro.valor).label("total")
        ).filter(
            LancamentoFinanceiro.tipo == "DESPESA",
            LancamentoFinanceiro.arquivado == False
        ).group_by(LancamentoFinanceiro.categoria).all()
        return resultados
    finally:
        session.close()
def listar_todas_cores_unicas():
    session = get_session()
    try:
        cores = session.query(CorProduto.nome, CorProduto.hex_cor).distinct().all()
        return {c.nome: c.hex_cor for c in cores}
    finally:
        session.close()
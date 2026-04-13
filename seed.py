from datetime import datetime, timedelta
from database import get_session, init_db
from models import Produto, MovimentacaoEstoque, LancamentoFinanceiro, CorProduto
import random
random.seed(42)
def popular_dados():
    session = get_session()
    try:
        if session.query(Produto).count() > 0:
            return False  
        hoje = datetime.now()
        produtos = [
            Produto(nome="Top Fitness Cruzado", categoria="Moda Feminina",
                    preco_custo=30.00, preco_venda=69.90, quantidade=50, estoque_minimo=10),
            Produto(nome="Legging Cintura Alta", categoria="Moda Feminina",
                    preco_custo=45.00, preco_venda=99.90, quantidade=80, estoque_minimo=15),
            Produto(nome="Camiseta Dry Fit", categoria="Moda Masculina",
                    preco_custo=25.00, preco_venda=59.90, quantidade=35, estoque_minimo=8),
            Produto(nome="Bermuda de Treino", categoria="Moda Masculina",
                    preco_custo=35.00, preco_venda=79.90, quantidade=20, estoque_minimo=5),
            Produto(nome="Garrafa Térmica 1L", categoria="Acessórios",
                    preco_custo=40.00, preco_venda=89.90, quantidade=100, estoque_minimo=20),
            Produto(nome="Bolsa de Academia", categoria="Acessórios",
                    preco_custo=60.00, preco_venda=149.90, quantidade=60, estoque_minimo=12),
        ]
        session.add_all(produtos)
        session.flush()
        cores = [
            CorProduto(produto_id=1, nome="Preto", hex_cor="#1a1a1a"),
            CorProduto(produto_id=1, nome="Rosa", hex_cor="#e91e8c"),
            CorProduto(produto_id=1, nome="Branco", hex_cor="#f5f5f5"),
            CorProduto(produto_id=2, nome="Preto", hex_cor="#1a1a1a"),
            CorProduto(produto_id=2, nome="Cinza", hex_cor="#6b7280"),
            CorProduto(produto_id=2, nome="Vinho", hex_cor="#7c2d3e"),
            CorProduto(produto_id=2, nome="Azul Marinho", hex_cor="#1e3a5f"),
            CorProduto(produto_id=3, nome="Branco", hex_cor="#f5f5f5"),
            CorProduto(produto_id=3, nome="Preto", hex_cor="#1a1a1a"),
            CorProduto(produto_id=3, nome="Verde Militar", hex_cor="#4a5d23"),
            CorProduto(produto_id=3, nome="Azul Royal", hex_cor="#2563eb"),
            CorProduto(produto_id=4, nome="Preto", hex_cor="#1a1a1a"),
            CorProduto(produto_id=4, nome="Cinza Escuro", hex_cor="#374151"),
            CorProduto(produto_id=5, nome="Preto", hex_cor="#1a1a1a"),
            CorProduto(produto_id=5, nome="Inox", hex_cor="#c0c0c0"),
            CorProduto(produto_id=5, nome="Rosa", hex_cor="#e91e8c"),
            CorProduto(produto_id=6, nome="Preto", hex_cor="#1a1a1a"),
            CorProduto(produto_id=6, nome="Azul", hex_cor="#2563eb"),
            CorProduto(produto_id=6, nome="Vermelho", hex_cor="#dc2626"),
        ]
        session.add_all(cores)
        session.flush()
        movimentacoes = [
            MovimentacaoEstoque(produto_id=1, tipo="ENTRADA", quantidade=30,
                                motivo="reposição", fornecedor="FitWear Distribuidora",
                                custo_total=900.00, data=hoje - timedelta(days=14)),
            MovimentacaoEstoque(produto_id=3, tipo="ENTRADA", quantidade=20,
                                motivo="reposição", fornecedor="Sports & Cia",
                                custo_total=500.00, data=hoje - timedelta(days=12)),
            MovimentacaoEstoque(produto_id=5, tipo="ENTRADA", quantidade=50,
                                motivo="reposição", fornecedor="Acessórios Fitness Atacado",
                                custo_total=2000.00, data=hoje - timedelta(days=10)),
            MovimentacaoEstoque(produto_id=2, tipo="ENTRADA", quantidade=40,
                                motivo="reposição", fornecedor="FitWear Distribuidora",
                                custo_total=1800.00, data=hoje - timedelta(days=8)),
            MovimentacaoEstoque(produto_id=1, tipo="SAÍDA", quantidade=8,
                                motivo="venda", data=hoje - timedelta(days=11)),
            MovimentacaoEstoque(produto_id=5, tipo="SAÍDA", quantidade=15,
                                motivo="venda", data=hoje - timedelta(days=9)),
            MovimentacaoEstoque(produto_id=3, tipo="SAÍDA", quantidade=5,
                                motivo="venda", data=hoje - timedelta(days=7)),
            MovimentacaoEstoque(produto_id=6, tipo="SAÍDA", quantidade=10,
                                motivo="venda", data=hoje - timedelta(days=5)),
            MovimentacaoEstoque(produto_id=4, tipo="SAÍDA", quantidade=3,
                                motivo="venda", data=hoje - timedelta(days=3)),
            MovimentacaoEstoque(produto_id=2, tipo="SAÍDA", quantidade=12,
                                motivo="venda", data=hoje - timedelta(days=1)),
        ]
        session.add_all(movimentacoes)
        lancamentos = [
            LancamentoFinanceiro(tipo="RECEITA", descricao="Venda: Top Fitness Cruzado (8 un.)",
                                 valor=559.20, categoria="Vendas",
                                 data=hoje - timedelta(days=11)),
            LancamentoFinanceiro(tipo="RECEITA", descricao="Venda: Garrafa Térmica 1L (15 un.)",
                                 valor=1348.50, categoria="Vendas",
                                 data=hoje - timedelta(days=9)),
            LancamentoFinanceiro(tipo="RECEITA", descricao="Venda: Camiseta Dry Fit (5 un.)",
                                 valor=299.50, categoria="Vendas",
                                 data=hoje - timedelta(days=7)),
            LancamentoFinanceiro(tipo="RECEITA", descricao="Venda: Bolsa de Academia (10 un.)",
                                 valor=1499.00, categoria="Vendas",
                                 data=hoje - timedelta(days=5)),
            LancamentoFinanceiro(tipo="RECEITA", descricao="Venda: Bermuda de Treino (3 un.)",
                                 valor=239.70, categoria="Vendas",
                                 data=hoje - timedelta(days=3)),
            LancamentoFinanceiro(tipo="DESPESA", descricao="Compra de estoque: Top Fitness Cruzado",
                                 valor=900.00, categoria="Compra de Estoque",
                                 data=hoje - timedelta(days=14)),
            LancamentoFinanceiro(tipo="DESPESA", descricao="Conta de energia elétrica",
                                 valor=285.00, categoria="Utilidades",
                                 data=hoje - timedelta(days=8)),
            LancamentoFinanceiro(tipo="DESPESA", descricao="Aluguel do espaço comercial",
                                 valor=1800.00, categoria="Aluguel",
                                 data=hoje - timedelta(days=6)),
        ]
        session.add_all(lancamentos)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
if __name__ == "__main__":
    init_db()
    if popular_dados():
        print("Dados iniciais inseridos com sucesso!")
    else:
        print(" Banco já contém dados. Nenhuma ação realizada.")
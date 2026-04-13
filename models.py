from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(200), nullable=False)
    categoria = Column(String(100), nullable=False)
    preco_custo = Column(Float, nullable=False)
    valor_compra = Column(Float, default=0.0)
    custos_variaveis = Column(Float, default=0.0)
    preco_venda = Column(Float, nullable=False)
    quantidade = Column(Integer, default=0)
    estoque_minimo = Column(Integer, default=5)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, default=datetime.now)
    atualizado_em = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    movimentacoes = relationship("MovimentacaoEstoque", back_populates="produto")
    cores = relationship("CorProduto", back_populates="produto", cascade="all, delete-orphan")
    @property
    def status(self):
        if self.quantidade <= 0:
            return "ESGOTADO"
        elif self.quantidade <= self.estoque_minimo:
            return "BAIXO"
        return "OK"
    def __repr__(self):
        return f"<Produto(id={self.id}, nome='{self.nome}', qtd={self.quantidade})>"
class MovimentacaoEstoque(Base):
    __tablename__ = "movimentacoes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    cor_id = Column(Integer, ForeignKey("cores_produto.id"), nullable=True)
    tamanho = Column(String(20), nullable=True)
    tipo = Column(String(10), nullable=False)  
    quantidade = Column(Integer, nullable=False)
    motivo = Column(String(100), nullable=True)  
    fornecedor = Column(String(200), nullable=True)
    custo_total = Column(Float, default=0.0)
    data = Column(DateTime, default=datetime.now)
    observacao = Column(String(500), nullable=True)
    produto = relationship("Produto", back_populates="movimentacoes")
    def __repr__(self):
        return f"<Movimentacao(id={self.id}, tipo='{self.tipo}', qtd={self.quantidade})>"
class CorProduto(Base):
    __tablename__ = "cores_produto"
    id = Column(Integer, primary_key=True, autoincrement=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    nome = Column(String(50), nullable=False)
    hex_cor = Column(String(7), nullable=False, default="#000000")
    quantidade = Column(Integer, default=0)
    qtd_p = Column(Integer, default=0)
    qtd_m = Column(Integer, default=0)
    qtd_g = Column(Integer, default=0)
    qtd_gg = Column(Integer, default=0)
    criado_em = Column(DateTime, default=datetime.now)
    produto = relationship("Produto", back_populates="cores")
    def __repr__(self):
        return f"<CorProduto(id={self.id}, nome='{self.nome}', hex='{self.hex_cor}')>"
class LancamentoFinanceiro(Base):
    __tablename__ = "lancamentos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(10), nullable=False)  
    descricao = Column(String(300), nullable=False)
    valor = Column(Float, nullable=False)
    categoria = Column(String(100), nullable=False)
    data = Column(DateTime, default=datetime.now)
    observacao = Column(String(500), nullable=True)
    arquivado = Column(Boolean, default=False)
    def __repr__(self):
        return f"<Lancamento(id={self.id}, tipo='{self.tipo}', valor={self.valor})>"
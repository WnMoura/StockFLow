from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "loja.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
def get_session():
    return SessionLocal()
def init_db():
    from models import Produto, MovimentacaoEstoque, LancamentoFinanceiro, CorProduto  
    Base.metadata.create_all(bind=engine)
"""
Configuração do banco de dados SQLite
Mudar para PostgreSQL no futuro
"""
from sqlmodel import create_engine, SQLModel, Session
import os

# URL do banco SQLite (arquivo local)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

# echo=True: mostra SQL no console 
# connect_args={"check_same_thread": False}: necessário para SQLite com FastAPI
engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)


def criar_tabelas():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

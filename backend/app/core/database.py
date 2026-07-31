from sqlmodel import create_engine, SQLModel, Session

from app.core.config import settings

# check_same_thread=False: o SQLite recusa uso da conexão fora da thread que a criou,
# e o FastAPI atende requisições em threads diferentes
connect_args = (
    {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
)

engine = create_engine(
    settings.database_url,
    echo=settings.sql_echo,
    connect_args=connect_args,
)


def criar_tabelas():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

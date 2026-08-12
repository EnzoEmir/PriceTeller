from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.core.database import get_session
from app.models.categoria import Categoria
from app.models.loja import Loja
from app.models.oferta import Oferta
from app.models.produto import Produto
from main import app


@pytest.fixture(name="session")
def session_fixture():
    # StaticPool mantém a mesma conexão em memória entre a fixture e o cliente
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session):
    app.dependency_overrides[get_session] = lambda: session
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture(name="catalogo")
def catalogo_fixture(session):
    """
    Cenário pequeno e explícito. Preços redondos para as asserções ficarem óbvias.

    Ryzen 7 5700X   Processador     Kabum 900,00  Pichau 850,00   menor 850
    Core i5-13400F  Processador     Kabum 1200,00                 menor 1200
    RTX 4060        Placa de Vídeo  Kabum 1900,00 Pichau 2000,00  menor 1900
    Sem Oferta      Placa de Vídeo  nenhuma                       sem preço
    """
    processador = Categoria(nome="Processador")
    video = Categoria(nome="Placa de Vídeo")
    kabum = Loja(nome="Kabum", url_base="https://kabum.com.br")
    pichau = Loja(nome="Pichau", url_base="https://pichau.com.br")
    session.add_all([processador, video, kabum, pichau])
    session.commit()

    ryzen = Produto(
        fk_categoria_id=processador.id,
        marca="AMD",
        modelo="Ryzen 7 5700X",
        ean="1111111111111",
        termos_busca=["R7 5700X"],
        specs={"socket": "AM4"},
    )
    intel = Produto(
        fk_categoria_id=processador.id,
        marca="Intel",
        modelo="Core i5-13400F",
        ean="2222222222222",
        termos_busca=["i5 13400F"],
    )
    rtx = Produto(
        fk_categoria_id=video.id,
        marca="Gigabyte",
        modelo="GeForce RTX 4060",
        ean="3333333333333",
        termos_busca=["RTX 4060 Eagle"],
    )
    sem_oferta = Produto(fk_categoria_id=video.id, marca="ZZZ", modelo="Sem Oferta")
    session.add_all([ryzen, intel, rtx, sem_oferta])
    session.commit()

    session.add_all(
        [
            Oferta(fk_produto_id=ryzen.id, fk_loja_id=kabum.id, preco_atual=Decimal("900.00"), url_link="https://kabum.com.br/ryzen"),
            Oferta(fk_produto_id=ryzen.id, fk_loja_id=pichau.id, preco_atual=Decimal("850.00"), url_link="https://pichau.com.br/ryzen"),
            Oferta(fk_produto_id=intel.id, fk_loja_id=kabum.id, preco_atual=Decimal("1200.00"), url_link="https://kabum.com.br/intel"),
            Oferta(fk_produto_id=rtx.id, fk_loja_id=kabum.id, preco_atual=Decimal("1900.00"), url_link="https://kabum.com.br/rtx"),
            Oferta(fk_produto_id=rtx.id, fk_loja_id=pichau.id, preco_atual=Decimal("2000.00"), url_link="https://pichau.com.br/rtx"),
        ]
    )
    session.commit()

    return {
        "categorias": {"processador": processador.id, "video": video.id},
        "produtos": {"ryzen": ryzen.id, "intel": intel.id, "rtx": rtx.id, "sem_oferta": sem_oferta.id},
    }

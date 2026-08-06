import os
os.environ["DATABASE_URL"] = "sqlite:///./seed.db"

from app.models.categoria import Categoria
from app.services.categoria_service import CategoriaService
from app.models.historico import Historico
from app.services.historico_service import HistoricoService
from app.models.loja import Loja
from app.services.loja_service import LojaService
from app.models.oferta import Oferta
from app.services.oferta_service import OfertaService
from app.models.produto import Produto
from app.services.produto_service import ProdutoService

# ==================== SETUP =====================
from faker import Faker
from app.test.factories.categoria_factory import make_categoria
from app.test.factories.loja_factory import make_loja
from app.test.factories.produto_factory import make_product
from app.test.factories.oferta_factory import make_oferta
from app.test.factories.historico_factory import make_history
fake = Faker('pt_BR')
from sqlmodel import Session

from app.core.database import engine, criar_tabelas, DATABASE_URL
print("==== hello ====")
print(DATABASE_URL)
print(engine.url)
criar_tabelas()

def get_session():
    with Session(engine) as session:
        yield session

# ==================== TESTES =====================
def test_criar_categoria():
    data = Categoria(**make_categoria())
    session = next(get_session())
    servicoCategoria = CategoriaService()
    servicoCategoria.criar_categoria(data, session=session)

def test_criar_loja():
    data = Loja(**make_loja())
    session = next(get_session())
    servicoLoja = LojaService()
    servicoLoja.criar_loja(data, session=session)

def test_criar_produto():
    session = next(get_session())

    categoria_service = CategoriaService()
    produto_service = ProdutoService()

    # Cria a categoria
    categoria = Categoria(**make_categoria())
    categoria_service.criar_categoria(categoria, session=session)

    # Cria o produto relacionado à categoria
    produto = Produto(
        fk_categoria_id=categoria.id,
        **make_product()
    )

    produto_service.criar_produto(produto, session=session)

    assert produto.id is not None
    assert produto.fk_categoria_id == categoria.id

def test_criar_oferta():
    session = next(get_session())

    categoria_service = CategoriaService()
    produto_service = ProdutoService()
    loja_service = LojaService()
    oferta_service = OfertaService()

    # Categoria
    categoria = Categoria(**make_categoria())
    categoria_service.criar_categoria(categoria, session)

    # Produto
    produto = Produto(
        fk_categoria_id=categoria.id,
        **make_product()
    )
    produto_service.criar_produto(produto, session)

    # Loja
    loja = Loja(**make_loja())
    loja_service.criar_loja(loja, session)

    # Oferta
    oferta = Oferta(
        fk_produto_id=produto.id,
        fk_loja_id=loja.id,
        **make_oferta()
    )
    oferta_service.criar_oferta(oferta, session)

    assert oferta.id is not None
    assert oferta.fk_produto_id == produto.id
    assert oferta.fk_loja_id == loja.id

def test_criar_historico():
    session = next(get_session())

    categoria_service = CategoriaService()
    produto_service = ProdutoService()
    loja_service = LojaService()
    oferta_service = OfertaService()
    historico_service = HistoricoService()

    # Categoria
    categoria = Categoria(**make_categoria())
    categoria_service.criar_categoria(categoria, session)

    # Produto
    produto = Produto(
        fk_categoria_id=categoria.id,
        **make_product()
    )
    produto_service.criar_produto(produto, session)

    # Loja
    loja = Loja(**make_loja())
    loja_service.criar_loja(loja, session)

    # Oferta
    oferta = Oferta(
        fk_produto_id=produto.id,
        fk_loja_id=loja.id,
        **make_oferta()
    )
    oferta_service.criar_oferta(oferta, session)

    # Histórico
    historico = Historico(
        fk_oferta_id=oferta.id,
        **make_history()
    )
    historico_service.criar_historico(historico, session)

    assert historico.id is not None
    assert historico.fk_oferta_id == oferta.id
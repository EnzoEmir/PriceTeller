from faker import Faker

fake = Faker('pt_BR')
from app.test.factories.categoria_factory import create_categoria
from app.test.factories.loja_factory import create_loja
from app.test.factories.produto_factory import create_produto
from app.test.factories.oferta_factory import create_oferta
from app.test.factories.historico_factory import create_historico

class ScenarioBuilder:
    def __init__(self, db):
        self.db = db

    def basic(self):
        categorias = [create_categoria(self.db) for _ in range(3)]
        lojas = [create_loja(self.db) for _ in range(3)]

        produtos = [
            create_produto(self.db, categoria=fake.random_element(categorias))
            for _ in range(10)
        ]

        ofertas = [
            create_oferta(self.db,
                produto=fake.random_element(produtos),
                loja=fake.random_element(lojas)
            )
            for _ in range(20)
        ]

        historicos = [
            create_historico(self.db, oferta=fake.random_element(ofertas))
            for _ in range(10)
        ]

        return {
            "categorias": categorias,
            "lojas": lojas,
            "produtos": produtos,
            "ofertas": ofertas,
            "historicos": historicos
        }
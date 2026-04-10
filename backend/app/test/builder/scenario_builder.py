from faker import Faker

fake = Faker('pt_BR')
from factories.categoria_factory import create_categoria
from factories.loja_factory import create_loja
from factories.produto_factory import create_produto
from factories.oferta_factory import create_oferta
from factories.historico_factory import create_historico

class ScenarioBuilder:
    def __init__(self, db):
        self.db = db

    def basic(self):
        categorias = [create_categoria() for _ in range(3)]
        lojas = [create_loja() for _ in range(3)]

        produtos = [
            create_produto(categoria=fake.random_element(categorias))
            for _ in range(10)
        ]

        ofertas = [
            create_oferta(self.db,
                produto=fake.random_element(produtos),
                loja=fake.random_element(lojas)
            )
            for _ in range(20)
        ]

        historicos = [create_historico() for _ in range(10)]

        return {
            "categorias": categorias,
            "lojas": lojas,
            "produtos": produtos,
            "ofertas": ofertas,
            "historicos": historicos
        }
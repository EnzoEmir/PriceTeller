from faker import Faker
from produto_factory import make_product
from loja_factory import make_loja

fake = Faker('pt_BR')

def make_oferta(product=None, loja=None, **overrides):
    product = product or make_product()
    loja = loja or make_loja()

    return {
        "id": fake.random_int(min=1, max=10000), #task: tirar id de factories e colocar em builders
        "marca": fake.word(),
        "modelo": fake.word(),
        # "produto_id": product["id"], #task: verificar como relacionar a oferta com produto em factory
        # "loja_id": loja["id"], #task: verificar como relacionar a oferta com a loja em factory
        **overrides
    }, product, loja
from faker import Faker
from produto_factory import make_product
from loja_factory import make_loja
from decimal import Decimal
from models.oferta import Oferta


fake = Faker('pt_BR')

def make_oferta(product=None, loja=None, **overrides):
    product = product or make_product()
    loja = loja or make_loja()

    return {
        # "id": fake.random_int(min=1, max=10000), #task: tirar id de factories e colocar em builders
        "marca": fake.word(),
        "modelo": fake.word(),
        # "produto_id": product["id"], #task: verificar como relacionar a oferta com produto em factory
        # "loja_id": loja["id"], #task: verificar como relacionar a oferta com a loja em factory
        **overrides
    }, product, loja

def create_oferta(db, produto, loja, **overrides):
    data = make_oferta(**overrides)

    oferta = Oferta(
        fk_produto_id=produto.id,
        fk_loja_id=loja.id,
        preco_atual=Decimal(data["preco"]),
        url_link=data["url_link"]
    )

    db.add(oferta)
    db.commit()
    db.refresh(oferta)

    return oferta
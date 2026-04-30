from faker import Faker
from app.test.factories.produto_factory import make_product
from app.test.factories.loja_factory import make_loja
from decimal import Decimal
from app.models.oferta import Oferta


fake = Faker('pt_BR')

def make_oferta(product=None, loja=None, **overrides):
    product = product or make_product()
    loja = loja or make_loja()

    return {
        # "id": fake.random_int(min=1, max=10000), #task: tirar id de factories e colocar em builders
        "preco": Decimal(str(fake.pydecimal(left_digits=4, right_digits=2, positive=True, min_value=10, max_value=5000))),
        "url_link": fake.url(),
        # "produto_id": product["id"], #task: verificar como relacionar a oferta com produto em factory
        # "loja_id": loja["id"], #task: verificar como relacionar a oferta com a loja em factory
        **overrides
    }

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
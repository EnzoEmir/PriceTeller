from faker import Faker
from app.test.factories.categoria_factory import make_categoria
from app.models.produto import Produto

fake = Faker('pt_BR')

def make_product(category=None, **overrides):
    category = category or make_categoria()

    return {
        # "id": fake.random_int(min=1, max=10000), #task: tirar id de factories e colocar em builders
        "marca": fake.word(),
        "modelo": fake.word(),
        # "category_id": category["id"], #task: verificar como relacionar o produto com categoria em factory
        **overrides
    }

def create_produto(db, categoria, **overrides):
    data = make_product(**overrides)

    produto = Produto(
        fk_categoria_id=categoria.id,
        marca=data["marca"],
        modelo=data["modelo"],
        specs=data.get("specs")
    )

    db.add(produto)
    db.commit()
    db.refresh(produto)

    return produto
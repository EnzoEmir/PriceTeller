from faker import Faker
from app.models.categoria import Categoria

fake = Faker('pt_BR')

def make_categoria(nome_length=None, **overrides):
    if nome_length is None:
        nome = fake.pystr(min_chars=1, max_chars=50)
    else:
        nome = fake.pystr(min_chars=nome_length, max_chars=nome_length)

    return {
        "nome": nome,
        **overrides
    }

def create_categoria(db, **overrides):
    data = make_categoria(**overrides)

    categoria = Categoria(
        nome=data["nome"]
    )

    db.add(categoria)
    db.commit()
    db.refresh(categoria)

    return categoria
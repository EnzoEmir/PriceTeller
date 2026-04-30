from faker import Faker
from app.models.loja import Loja

fake = Faker('pt_BR')

def make_loja(nome_length=None, url_base_length=None, **overrides):
    if nome_length is None:
        nome = fake.pystr(min_chars=1, max_chars=50)
    else:
        nome = fake.pystr(min_chars=nome_length, max_chars=nome_length)

    if url_base_length is None:
        url_base = fake.pystr(min_chars=1, max_chars=50)
    else:
        url_base = fake.pystr(min_chars=url_base_length, max_chars=url_base_length)

    return {
        "nome": nome,
        "url_base": url_base,
        **overrides
    }

def create_loja(db, **overrides):
    data = make_loja(**overrides)

    loja = Loja(
        nome=data["nome"],
        url_base=data["url_base"]
    )

    db.add(loja)
    db.commit()
    db.refresh(loja)

    return loja
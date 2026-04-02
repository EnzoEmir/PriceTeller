from faker import Faker

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
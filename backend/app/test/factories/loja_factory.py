from faker import Faker

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
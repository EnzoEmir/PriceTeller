from faker import Faker
from oferta_factory import make_oferta


fake = Faker('pt_BR')

def make_history(oferta=None, **overrides):
    oferta = oferta or make_oferta()

    return {
        "id": fake.random_int(min=1, max=10000), #task: tirar id de factories e colocar em builders
        "preco": fake.pyfloat(left_digits=4, right_digits=2, positive=True, min_value=10.0, max_value=5000.0),
        "data": fake.date_between(start_date='-5y', end_date='today'),
        # "fk_oferta_id": oferta["id"], #task: verificar como relacionar a oferta com produto em factory
        **overrides
    }, oferta
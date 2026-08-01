import random
import re
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from faker import Faker
from sqlmodel import select

fake = Faker('pt_BR')
from app.data.loader import carregar_catalogo
from app.models.categoria import Categoria
from app.models.loja import Loja
from app.models.oferta import Oferta
from app.models.produto import Produto
from app.test.factories.categoria_factory import create_categoria
from app.test.factories.loja_factory import create_loja
from app.test.factories.produto_factory import create_produto
from app.test.factories.oferta_factory import create_oferta
from app.test.factories.historico_factory import create_historico

LOJAS = [
    ("Kabum", "https://www.kabum.com.br"),
    ("Pichau", "https://www.pichau.com.br"),
    ("Terabyte Shop", "https://www.terabyteshop.com.br"),
    ("Amazon", "https://www.amazon.com.br"),
]

# Ancoram o preço do teste em algo plausível.
PRECOS_REFERENCIA = {
    "Ryzen 7 5700X": 950,
    "Ryzen 5 7600": 1250,
    "Core i5-13400F": 1100,
    "Core i7-14700K": 2600,
    "TUF Gaming B550M-Plus": 780,
    "B650 Gaming Plus WiFi": 1350,
    "B760M AORUS Elite": 1150,
    "B450M Steel Legend": 550,
    "GeForce RTX 4060 Eagle OC 8G": 1900,
    "GeForce RTX 4070 Super Ventus 2X OC 12G": 4200,
    "Dual Radeon RX 6600 V2 8GB": 1350,
    "Pulse Radeon RX 7800 XT 16GB": 3600,
    "Fury Beast 16GB (1x16GB) 3200MHz": 280,
    "Vengeance LPX 16GB (2x8GB) 3600MHz": 340,
    "Ripjaws S5 32GB (2x16GB) 6000MHz": 780,
    "Lancer RGB 32GB (2x16GB) 6000MHz": 850,
    "CV650": 380,
    "MAG A650BN": 350,
    "Core Reactor 750W": 650,
    "MWE Gold 850 V2": 780,
}

FAIXA_POR_CATEGORIA = {
    "Processador": (700, 3500),
    "Placa de Vídeo": (1300, 7000),
    "Placa-Mãe": (500, 2200),
    "Memória RAM": (200, 1200),
    "Fonte": (280, 900),
}


def _slug(texto: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", texto.lower()).strip("-")


def _preco(valor: float) -> Decimal:
    return Decimal(f"{int(valor)}.90")


class ScenarioBuilder:
    def __init__(self, db):
        self.db = db

    def basic(self):
        categorias = [create_categoria(self.db) for _ in range(3)]
        lojas = [create_loja(self.db) for _ in range(3)]

        produtos = [
            create_produto(self.db, categoria=fake.random_element(categorias))
            for _ in range(10)
        ]

        ofertas = [
            create_oferta(self.db,
                produto=fake.random_element(produtos),
                loja=fake.random_element(lojas)
            )
            for _ in range(20)
        ]

        historicos = [
            create_historico(self.db, oferta=fake.random_element(ofertas))
            for _ in range(10)
        ]

        return {
            "categorias": categorias,
            "lojas": lojas,
            "produtos": produtos,
            "ofertas": ofertas,
            "historicos": historicos
        }

    def catalogo_com_ofertas(self, pontos_historico=6):
        resumo = carregar_catalogo(self.db)
        lojas = self._resolver_lojas()
        categorias = {c.id: c.nome for c in self.db.exec(select(Categoria)).all()}

        criadas = 0
        existentes = 0

        for produto in self.db.exec(select(Produto)).all():
            # semente derivada do produto: rodar de novo reproduz os mesmos preços
            rng = random.Random(f"produto-{produto.id}")
            base = self._preco_base(produto, categorias, rng)

            for loja in rng.sample(lojas, rng.randint(2, min(3, len(lojas)))):
                url_link = f"{loja.url_base}/produto/{produto.id}-{_slug(produto.modelo)}"

                if self.db.exec(select(Oferta).where(Oferta.url_link == url_link)).first():
                    existentes += 1
                    continue

                preco = _preco(base * rng.uniform(0.92, 1.10))
                oferta = create_oferta(
                    self.db, produto=produto, loja=loja, preco=preco, url_link=url_link
                )
                self._gerar_historico(oferta, preco, rng, pontos_historico)
                criadas += 1

        return {
            **resumo,
            "lojas": len(lojas),
            "ofertas_criadas": criadas,
            "ofertas_existentes": existentes,
        }

    def _resolver_lojas(self):
        lojas = []

        for nome, url_base in LOJAS:
            loja = self.db.exec(select(Loja).where(Loja.nome == nome)).first()
            if loja is None:
                loja = Loja(nome=nome, url_base=url_base)
                self.db.add(loja)
                self.db.commit()
                self.db.refresh(loja)
            lojas.append(loja)

        return lojas

    def _preco_base(self, produto, categorias, rng):
        if produto.modelo in PRECOS_REFERENCIA:
            return PRECOS_REFERENCIA[produto.modelo]

        faixa = FAIXA_POR_CATEGORIA.get(categorias.get(produto.fk_categoria_id), (200, 2000))
        return rng.uniform(*faixa)

    def _gerar_historico(self, oferta, preco_atual, rng, pontos):
        agora = datetime.now(timezone.utc)

        for meses_atras in range(pontos, 0, -1):
            create_historico(
                self.db,
                oferta=oferta,
                preco=_preco(float(preco_atual) * rng.uniform(0.90, 1.18)),
                data=agora - timedelta(days=meses_atras * 30),
            )

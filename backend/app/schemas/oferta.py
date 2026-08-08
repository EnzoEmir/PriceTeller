from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel


class MelhorOferta(SQLModel):
    loja_id: int
    loja_nome: str
    preco: Decimal
    url_link: str


class ResumoOfertas(SQLModel):
    total_ofertas: int = 0
    melhor_oferta: Optional[MelhorOferta] = None

from decimal import Decimal
from typing import Optional

from pydantic import Field
from sqlmodel import SQLModel

from app.schemas.tipos import Preco, UrlHttp


class OfertaBase(SQLModel):
    fk_produto_id: int
    fk_loja_id: int
    preco_atual: Preco
    url_link: UrlHttp


class OfertaCreate(OfertaBase):
    pass


class OfertaUpdate(OfertaBase):
    pass


class OfertaRead(OfertaBase):
    id: int


class OfertaDaLoja(SQLModel):
    loja_id: int
    loja_nome: str
    preco: Decimal
    url_link: str


class ResumoOfertas(SQLModel):
    # da mais barata para a mais cara; `melhor_oferta` é a primeira, repetida
    # para o consumidor que só quer o destaque não depender da ordem
    ofertas: list[OfertaDaLoja] = Field(default_factory=list)
    melhor_oferta: Optional[OfertaDaLoja] = None

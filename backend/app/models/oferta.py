from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Numeric
from decimal import Decimal
from typing import Optional


class Oferta(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fk_produto_id: int = Field(foreign_key="produto.id")
    fk_loja_id: int = Field(foreign_key="loja.id")
    preco_atual: Decimal = Field(sa_column=Column(Numeric(10, 2)))
    url_link: str

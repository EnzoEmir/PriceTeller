from sqlmodel import SQLModel, Field
from typing import Optional


class Loja(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100)
    url_base: str
    
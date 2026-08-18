from sqlmodel import Field, SQLModel

from app.schemas.tipos import UrlHttp


class LojaBase(SQLModel):
    nome: str = Field(min_length=1, max_length=100)
    url_base: UrlHttp


class LojaCreate(LojaBase):
    pass


class LojaUpdate(LojaBase):
    pass


class LojaRead(LojaBase):
    id: int

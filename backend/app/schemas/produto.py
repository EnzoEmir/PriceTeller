from typing import Any, Dict, List, Optional

from sqlmodel import SQLModel

from app.schemas.oferta import ResumoOfertas


class ProdutoBase(SQLModel):
    fk_categoria_id: int
    marca: str
    modelo: str
    ean: Optional[str] = None
    termos_busca: Optional[List[str]] = None
    specs: Optional[Dict[str, Any]] = None


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoUpdate(ProdutoBase):
    pass


class ProdutoRead(ProdutoBase):
    id: int


class ProdutoComOfertas(ProdutoRead, ResumoOfertas):
    @classmethod
    def montar(cls, produto, resumo: Optional[ResumoOfertas] = None) -> "ProdutoComOfertas":
        resumo = resumo or ResumoOfertas()
        return cls(**produto.model_dump(), **resumo.model_dump())

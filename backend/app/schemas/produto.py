from typing import Any, Dict, List, Optional

from sqlmodel import SQLModel


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

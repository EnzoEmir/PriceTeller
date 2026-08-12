from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from typing import Optional, Dict, Any, List


class Produto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fk_categoria_id: int = Field(foreign_key="categoria.id")
    marca: str = Field(max_length=100)
    modelo: str = Field(max_length=255)
    ean: Optional[str] = Field(default=None, max_length=13, unique=True, index=True)
    # nomes alternativos usados pelas lojas, para casar anúncio com produto na importação
    termos_busca: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    specs: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    
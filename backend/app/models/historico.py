from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Numeric
from decimal import Decimal
from datetime import datetime, timezone
from typing import Optional


class Historico(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fk_oferta_id: int = Field(foreign_key="oferta.id")
    preco: Decimal = Field(sa_column=Column(Numeric(10, 2)))
    data: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
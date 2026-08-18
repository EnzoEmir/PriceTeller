from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel

from app.schemas.tipos import Preco


class HistoricoBase(SQLModel):
    fk_oferta_id: int
    preco: Preco


class HistoricoCreate(HistoricoBase):
    # ausente, o carimbo vem do default_factory do modelo
    data: Optional[datetime] = None


class HistoricoUpdate(HistoricoCreate):
    pass


class HistoricoRead(HistoricoBase):
    id: int
    data: datetime

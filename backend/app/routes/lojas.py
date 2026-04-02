from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.core.database import get_session
from app.models.loja import Loja
from app.services.loja_service import LojaService

router = APIRouter(prefix="/lojas", tags=["Lojas"])

servicoLoja = LojaService()

@router.post("/", response_model=Loja, status_code=201)
def criar_loja(
    loja: Loja, 
    session: Session = Depends(get_session)
):
    return servicoLoja.criar_loja(loja, session)

@router.get("/", response_model=List[Loja])
def listar_lojas(session: Session = Depends(get_session)):
    return servicoLoja.listar_lojas(session)


@router.get("/{loja_id}", response_model=Loja)
def buscar_loja(loja_id: int, session: Session = Depends(get_session)):
    return servicoLoja.buscar_loja(loja_id, session)


@router.put("/{loja_id}", response_model=Loja)
def atualizar_loja(
        loja_id: int,
        loja_atualizada: Loja,
        session: Session = Depends(get_session)
    ):
        return servicoLoja.atualizar_loja(loja_id, loja_atualizada, session)

@router.delete("/{loja_id}", status_code=204)
def deletar_loja(loja_id: int, session: Session = Depends(get_session)):
    return servicoLoja.deletar_loja(loja_id, session)
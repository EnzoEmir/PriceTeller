from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.core.database import get_session
from app.models.historico import Historico
from app.services.historico_service import HistoricoService

router = APIRouter(prefix="/historico", tags=["Historico"])

servicoHistorico = HistoricoService()


@router.post("/", response_model=Historico, status_code=201)
def criar_historico(
    historico: Historico,
    session: Session = Depends(get_session),
):
    return servicoHistorico.criar_historico(historico, session)


@router.get("/", response_model=List[Historico])
def listar_historico(
    session: Session = Depends(get_session)
):
    return servicoHistorico.listar_historico(session)

@router.get("/{historico_id}", response_model=Historico)
def buscar_historico(
    historico_id: int, 
    session: Session = Depends(get_session)
):
    return servicoHistorico.buscar_historico(historico_id, session)


@router.put("/{historico_id}", response_model=Historico)
def atualizar_historico(
        historico_id: int,
        historico_atualizado: Historico,
        session: Session = Depends(get_session)
):
    return servicoHistorico.atualizar_historico(historico_id, historico_atualizado, session)


@router.delete("/{historico_id}", status_code=204)
def deletar_historico(
    historico_id: int,
    session: Session = Depends(get_session)
):
    servicoHistorico.deletar_historico(historico_id, session)

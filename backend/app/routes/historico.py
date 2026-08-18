from fastapi import APIRouter, Depends, Request 
from sqlmodel import Session
from typing import List

from app.core.database import get_session
from app.core.security import exigir_api_key
from app.models.historico import Historico
from app.schemas.historico import HistoricoCreate, HistoricoRead, HistoricoUpdate
from app.services.historico_service import HistoricoService
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter(prefix="/historico", tags=["Historico"])

# Cria um limiter específico para este módulo
limiter = Limiter(key_func=get_remote_address)
servicoHistorico = HistoricoService()

# Constantes para facilitar manutenção
CREATE_LIMIT = "5/minute"      # 5 criações por minuto
READ_LIMIT = "100/minute"      # 100 leituras por minuto
UPDATE_LIMIT = "10/minute"     # 10 atualizações por minuto
DELETE_LIMIT = "3/minute"      # 3 deleções por minuto

@router.post(
    "/",
    response_model=HistoricoRead,
    status_code=201,
    dependencies=[Depends(exigir_api_key)],
)
@limiter.limit(CREATE_LIMIT)
def criar_historico(
    request: Request,
    historico: HistoricoCreate,
    session: Session = Depends(get_session),
):
    return servicoHistorico.criar_historico(
        Historico(**historico.model_dump(exclude_none=True)), session
    )


@router.get("/", response_model=List[HistoricoRead])
@limiter.limit(READ_LIMIT)
def listar_historico(
    request: Request,
    session: Session = Depends(get_session)
):
    return servicoHistorico.listar_historico(session)


@router.get("/{historico_id}", response_model=HistoricoRead)
@limiter.limit(READ_LIMIT)
def buscar_historico(
    request: Request,
    historico_id: int, 
    session: Session = Depends(get_session)
):
    return servicoHistorico.buscar_historico(historico_id, session)


@router.put(
    "/{historico_id}",
    response_model=HistoricoRead,
    dependencies=[Depends(exigir_api_key)],
)
@limiter.limit(UPDATE_LIMIT)
def atualizar_historico(
    request: Request,
    historico_id: int,
    historico_atualizado: HistoricoUpdate,
    session: Session = Depends(get_session)
):
    return servicoHistorico.atualizar_historico(
        historico_id,
        Historico(**historico_atualizado.model_dump(exclude_none=True)),
        session,
    )


@router.delete(
    "/{historico_id}",
    status_code=204,
    dependencies=[Depends(exigir_api_key)],
)
@limiter.limit(DELETE_LIMIT)
def deletar_historico(
    request: Request,
    historico_id: int,
    session: Session = Depends(get_session)
):
    servicoHistorico.deletar_historico(historico_id, session)
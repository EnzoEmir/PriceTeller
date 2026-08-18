from fastapi import APIRouter, Depends, Request
from sqlmodel import Session
from typing import List

from app.core.database import get_session
from app.core.security import exigir_api_key
from app.models.loja import Loja
from app.schemas.loja import LojaCreate, LojaRead, LojaUpdate
from app.services.loja_service import LojaService
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter(prefix="/lojas", tags=["Lojas"])

# Cria um limiter específico para este módulo
limiter = Limiter(key_func=get_remote_address)
servicoLoja = LojaService()

# Constantes para facilitar manutenção
CREATE_LIMIT = "5/minute"      # 5 criações por minuto
READ_LIMIT = "120/minute"      # 120 leituras por minuto (lojas são consultadas com frequência)
UPDATE_LIMIT = "10/minute"     # 10 atualizações por minuto
DELETE_LIMIT = "3/minute"      # 3 deleções por minuto

@router.post(
    "/",
    response_model=LojaRead,
    status_code=201,
    dependencies=[Depends(exigir_api_key)],
)
@limiter.limit(CREATE_LIMIT)
def criar_loja(
    request: Request,
    loja: LojaCreate,
    session: Session = Depends(get_session)
):
    return servicoLoja.criar_loja(Loja(**loja.model_dump()), session)


@router.get("/", response_model=List[LojaRead])
@limiter.limit(READ_LIMIT)
def listar_lojas(
    request: Request,
    session: Session = Depends(get_session)
):
    return servicoLoja.listar_lojas(session)


@router.get("/{loja_id}", response_model=LojaRead)
@limiter.limit(READ_LIMIT)
def buscar_loja(
    request: Request,
    loja_id: int, 
    session: Session = Depends(get_session)
):
    return servicoLoja.buscar_loja(loja_id, session)


@router.put(
    "/{loja_id}",
    response_model=LojaRead,
    dependencies=[Depends(exigir_api_key)],
)
@limiter.limit(UPDATE_LIMIT)
def atualizar_loja(
    request: Request,
    loja_id: int,
    loja_atualizada: LojaUpdate,
    session: Session = Depends(get_session)
):
    return servicoLoja.atualizar_loja(loja_id, Loja(**loja_atualizada.model_dump()), session)


@router.delete(
    "/{loja_id}",
    status_code=204,
    dependencies=[Depends(exigir_api_key)],
)
@limiter.limit(DELETE_LIMIT)
def deletar_loja(
    request: Request,
    loja_id: int, 
    session: Session = Depends(get_session)
):
    return servicoLoja.deletar_loja(loja_id, session)
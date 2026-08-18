from fastapi import APIRouter, Depends, Request
from sqlmodel import Session
from typing import List

from app.core.database import get_session
from app.core.security import exigir_api_key
from app.models.oferta import Oferta
from app.schemas.oferta import OfertaCreate, OfertaRead, OfertaUpdate
from app.services.oferta_service import OfertaService
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter(prefix="/ofertas", tags=["Ofertas"])

# Cria um limiter específico para este módulo
limiter = Limiter(key_func=get_remote_address)
servicoOferta = OfertaService()

# Constantes para facilitar manutenção
CREATE_LIMIT = "3/minute"      # 3 criações por minuto (mais restritivo)
READ_LIMIT = "80/minute"       # 80 leituras por minuto
UPDATE_LIMIT = "8/minute"      # 8 atualizações por minuto
DELETE_LIMIT = "2/minute"      # 2 deleções por minuto

@router.post(
    "/",
    response_model=OfertaRead,
    status_code=201,
    dependencies=[Depends(exigir_api_key)],
)
@limiter.limit(CREATE_LIMIT)
def criar_oferta(
    request: Request,
    oferta: OfertaCreate,
    session: Session = Depends(get_session)
):
    return servicoOferta.criar_oferta(Oferta(**oferta.model_dump()), session)


@router.get("/", response_model=List[OfertaRead])
@limiter.limit(READ_LIMIT)
def listar_ofertas(
    request: Request,
    session: Session = Depends(get_session)
):
    return servicoOferta.listar_ofertas(session)


@router.get("/{oferta_id}", response_model=OfertaRead)
@limiter.limit(READ_LIMIT)
def buscar_oferta(
    request: Request,
    oferta_id: int, 
    session: Session = Depends(get_session)
):
    return servicoOferta.buscar_oferta(oferta_id, session)


@router.put(
    "/{oferta_id}",
    response_model=OfertaRead,
    dependencies=[Depends(exigir_api_key)],
)
@limiter.limit(UPDATE_LIMIT)
def atualizar_oferta(
    request: Request,
    oferta_id: int,
    oferta_atualizada: OfertaUpdate,
    session: Session = Depends(get_session)
):
    return servicoOferta.atualizar_oferta(
        oferta_id, Oferta(**oferta_atualizada.model_dump()), session
    )


@router.delete(
    "/{oferta_id}",
    status_code=204,
    dependencies=[Depends(exigir_api_key)],
)
@limiter.limit(DELETE_LIMIT)
def deletar_oferta(
    request: Request,
    oferta_id: int, 
    session: Session = Depends(get_session)
):
    return servicoOferta.deletar_oferta(oferta_id, session)
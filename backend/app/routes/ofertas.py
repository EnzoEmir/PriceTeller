from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.core.database import get_session
from app.models.oferta import Oferta
from app.services.oferta_service import OfertaService

router = APIRouter(prefix="/ofertas", tags=["Ofertas"])

servicoOferta = OfertaService()

@router.post("/", response_model=Oferta, status_code=201)
def criar_oferta(oferta: Oferta, session: Session = Depends(get_session)):
    return servicoOferta.criar_oferta(oferta, session)


@router.get("/", response_model=List[Oferta])
def listar_ofertas(session: Session = Depends(get_session)):
    return servicoOferta.listar_ofertas(session)


@router.get("/{oferta_id}", response_model=Oferta)
def buscar_oferta(oferta_id: int, session: Session = Depends(get_session)):
    return servicoOferta.buscar_oferta(oferta_id, session)


@router.put("/{oferta_id}", response_model=Oferta)
def atualizar_oferta(
        oferta_id: int,
        oferta_atualizada: Oferta,
        session: Session = Depends(get_session)
    ):
    return servicoOferta.atualizar_oferta(oferta_id, oferta_atualizada, session)


@router.delete("/{oferta_id}", status_code=204)
def deletar_oferta(oferta_id: int, session: Session = Depends(get_session)):
     return servicoOferta.deletar_oferta(oferta_id, session)

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from app.core.database import get_session
from app.models.oferta import Oferta

router = APIRouter(prefix="/ofertas", tags=["Ofertas"])


@router.post("/", response_model=Oferta, status_code=201)
def criar_oferta(oferta: Oferta, session: Session = Depends(get_session)):
    """
    Cria uma nova oferta no banco de dados.
    
    - **fk_produto_id**: ID do produto
    - **fk_loja_id**: ID da loja
    - **preco_atual**: Preço atual do produto (use string: "1299.90")
    - **url_link**: Link direto para o produto na loja
    """
    session.add(oferta)
    session.commit()
    session.refresh(oferta)
    return oferta


@router.get("/", response_model=List[Oferta])
def listar_ofertas(session: Session = Depends(get_session)):
    """
    Retorna todas as ofertas cadastradas.
    """
    statement = select(Oferta)
    ofertas = session.exec(statement).all()
    return ofertas


@router.get("/{oferta_id}", response_model=Oferta)
def buscar_oferta(oferta_id: int, session: Session = Depends(get_session)):
    """
    Busca uma oferta específica por ID.
    
    - **oferta_id**: ID da oferta
    """
    oferta = session.get(Oferta, oferta_id)
    
    if not oferta:
        raise HTTPException(status_code=404, detail="Oferta não encontrada")
    
    return oferta

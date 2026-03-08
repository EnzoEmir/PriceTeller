from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from app.core.database import get_session
from app.models.categoria import Categoria

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.post("/", response_model=Categoria, status_code=201)
def criar_categoria(categoria: Categoria, session: Session = Depends(get_session)):
    """
    Cria uma nova categoria no banco de dados.
    
    - **nome**: Nome da categoria (ex: 'Processador', 'Placa de Vídeo')
    """
    session.add(categoria)
    session.commit()
    session.refresh(categoria)  
    return categoria


@router.get("/", response_model=List[Categoria])
def listar_categorias(session: Session = Depends(get_session)):
    """
    Retorna todas as categorias cadastradas.
    """
    statement = select(Categoria)
    categorias = session.exec(statement).all()
    return categorias


@router.get("/{categoria_id}", response_model=Categoria)
def buscar_categoria(categoria_id: int, session: Session = Depends(get_session)):
    """
    Busca uma categoria específica por ID.
    
    - **categoria_id**: ID da categoria
    """
    categoria = session.get(Categoria, categoria_id)
    
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    return categoria

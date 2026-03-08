from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from app.core.database import get_session
from app.models.produto import Produto

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.post("/", response_model=Produto, status_code=201)
def criar_produto(produto: Produto, session: Session = Depends(get_session)):
    """
    Cria um novo produto no banco de dados.
    
    - **fk_categoria_id**: ID da categoria
    - **marca**: Fabricante (ex: 'Intel', 'NVIDIA', 'AMD')
    - **modelo**: Modelo completo (ex: 'Core i7-13700K', 'RTX 4070 Ti')
    - **specs**: Especificações técnicas (JSON, opcional)
    """
    session.add(produto)
    session.commit()
    session.refresh(produto)
    return produto


@router.get("/", response_model=List[Produto])
def listar_produtos(session: Session = Depends(get_session)):
    """
    Retorna todos os produtos cadastrados.
    """
    statement = select(Produto)
    produtos = session.exec(statement).all()
    return produtos


@router.get("/{produto_id}", response_model=Produto)
def buscar_produto(produto_id: int, session: Session = Depends(get_session)):
    """
    Busca um produto específico por ID.
    
    - **produto_id**: ID do produto
    """
    produto = session.get(Produto, produto_id)
    
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return produto

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from app.core.database import get_session
from app.models.produto import Produto
from app.services.produto_service import ProdutoService

router = APIRouter(prefix="/produtos", tags=["Produtos"])

servicoProduto = ProdutoService()

@router.post("/", response_model=Produto, status_code=201)
def criar_produto(produto: Produto, session: Session = Depends(get_session)):
    return servicoProduto.criar_produto(produto, session)


@router.get("/", response_model=List[Produto])
def listar_produtos(session: Session = Depends(get_session)):
    return servicoProduto.listar_produtos(session)


@router.get("/{produto_id}", response_model=Produto)
def buscar_produto(produto_id: int, session: Session = Depends(get_session)):
    return servicoProduto.buscar_produto(produto_id, session)


@router.put("/{produto_id}", response_model=Produto)
def atualizar_produto(
        produto_id: int,
        produto_atualizado: Produto,
        session: Session = Depends(get_session)
    ):
        return servicoProduto.atualizar_produto(produto_id, produto_atualizado, session)


@router.delete("/{produto_id}", status_code=204)
def deletar_produto(produto_id: int, session: Session = Depends(get_session)):
    return servicoProduto.deletar_produto(produto_id, session)

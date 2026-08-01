from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.core.database import get_session
from app.models.produto import Produto
from app.schemas.produto import ProdutoCreate, ProdutoRead, ProdutoUpdate
from app.services.produto_service import ProdutoService

router = APIRouter(prefix="/produtos", tags=["Produtos"])

servicoProduto = ProdutoService()

@router.post("/", response_model=ProdutoRead, status_code=201)
def criar_produto(produto: ProdutoCreate, session: Session = Depends(get_session)):
    return servicoProduto.criar_produto(Produto(**produto.model_dump()), session)


@router.get("/", response_model=List[ProdutoRead])
def listar_produtos(session: Session = Depends(get_session)):
    return servicoProduto.listar_produtos(session)


@router.get("/{produto_id}", response_model=ProdutoRead)
def buscar_produto(produto_id: int, session: Session = Depends(get_session)):
    return servicoProduto.buscar_produto(produto_id, session)


@router.put("/{produto_id}", response_model=ProdutoRead)
def atualizar_produto(
        produto_id: int,
        produto_atualizado: ProdutoUpdate,
        session: Session = Depends(get_session)
    ):
        return servicoProduto.atualizar_produto(
            produto_id, Produto(**produto_atualizado.model_dump()), session
        )


@router.delete("/{produto_id}", status_code=204)
def deletar_produto(produto_id: int, session: Session = Depends(get_session)):
    return servicoProduto.deletar_produto(produto_id, session)

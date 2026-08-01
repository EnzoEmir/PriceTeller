from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.core.database import get_session
from app.models.produto import Produto
from app.schemas.pagina import Pagina
from app.schemas.produto import ProdutoComOfertas, ProdutoCreate, ProdutoRead, ProdutoUpdate
from app.services.oferta_service import OfertaService
from app.services.produto_service import ProdutoService

router = APIRouter(prefix="/produtos", tags=["Produtos"])

servicoProduto = ProdutoService()
servicoOferta = OfertaService()

@router.post("/", response_model=ProdutoRead, status_code=201)
def criar_produto(produto: ProdutoCreate, session: Session = Depends(get_session)):
    return servicoProduto.criar_produto(Produto(**produto.model_dump()), session)


@router.get("/", response_model=Pagina[ProdutoComOfertas])
def listar_produtos(
    page: int = Query(1, ge=1, description="Número da página, começando em 1"),
    limit: int = Query(20, ge=1, le=100, description="Produtos por página"),
    q: Optional[str] = Query(None, description="Busca em marca, modelo e termos de busca"),
    categoria_id: Optional[int] = Query(None, description="Filtra por categoria"),
    session: Session = Depends(get_session),
):
    produtos, total = servicoProduto.listar_produtos(session, page, limit, q, categoria_id)
    resumos = servicoOferta.resumo_por_produto(session, [p.id for p in produtos])
    items = [ProdutoComOfertas.montar(p, resumos.get(p.id)) for p in produtos]
    return Pagina.criar(items=items, total=total, page=page, limit=limit)


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

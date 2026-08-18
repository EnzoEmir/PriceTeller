from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, Query, Request
from sqlmodel import Session

from app.core.database import get_session
from app.core.security import exigir_api_key
from app.models.produto import Produto
from app.schemas.pagina import Pagina
from app.schemas.produto import (
    OrdenacaoProduto,
    ProdutoComOfertas,
    ProdutoCreate,
    ProdutoRead,
    ProdutoUpdate,
)
from app.services.oferta_service import OfertaService
from app.services.produto_service import ProdutoService
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter(prefix="/produtos", tags=["Produtos"])

# Cria um limiter específico para este módulo
limiter = Limiter(key_func=get_remote_address)

servicoProduto = ProdutoService()
servicoOferta = OfertaService()

# Constantes para facilitar manutenção
CREATE_LIMIT = "5/minute"       # 5 criações por minuto
READ_LIMIT = "60/minute"        # 60 leituras por minuto (produtos são pesados)
READ_LIST_LIMIT = "40/minute"   # 40 listagens por minuto (com filtros, é mais pesado)
UPDATE_LIMIT = "10/minute"      # 10 atualizações por minuto
DELETE_LIMIT = "3/minute"       # 3 deleções por minuto

@router.post(
    "/",
    response_model=ProdutoRead,
    status_code=201,
    dependencies=[Depends(exigir_api_key)],
)
@limiter.limit(CREATE_LIMIT)
def criar_produto(
    request: Request,
    produto: ProdutoCreate, 
    session: Session = Depends(get_session)
):
    return servicoProduto.criar_produto(Produto(**produto.model_dump()), session)


@router.get("/", response_model=Pagina[ProdutoComOfertas])
@limiter.limit(READ_LIST_LIMIT)  # Limite menor pois a consulta é complexa
def listar_produtos(
    request: Request,
    page: int = Query(1, ge=1, description="Número da página, começando em 1"),
    limit: int = Query(20, ge=1, le=100, description="Produtos por página"),
    q: Optional[str] = Query(None, description="Busca em marca, modelo e termos de busca"),
    categoria_id: Optional[int] = Query(None, description="Filtra por categoria"),
    preco_min: Optional[Decimal] = Query(None, ge=0, description="Preço mínimo da oferta mais barata"),
    preco_max: Optional[Decimal] = Query(None, ge=0, description="Preço máximo da oferta mais barata"),
    ordenar: OrdenacaoProduto = Query(OrdenacaoProduto.padrao, description="Ordem dos resultados"),
    session: Session = Depends(get_session),
):
    produtos, total = servicoProduto.listar_produtos(
        session, page, limit, q, categoria_id, preco_min, preco_max, ordenar
    )
    resumos = servicoOferta.resumo_por_produto(session, [p.id for p in produtos])
    items = [ProdutoComOfertas.montar(p, resumos.get(p.id)) for p in produtos]
    return Pagina.criar(items=items, total=total, page=page, limit=limit)


@router.get("/{produto_id}", response_model=ProdutoRead)
@limiter.limit(READ_LIMIT)
def buscar_produto(
    request: Request,
    produto_id: int, 
    session: Session = Depends(get_session)
):
    return servicoProduto.buscar_produto(produto_id, session)


@router.put(
    "/{produto_id}",
    response_model=ProdutoRead,
    dependencies=[Depends(exigir_api_key)],
)
@limiter.limit(UPDATE_LIMIT)
def atualizar_produto(
    request: Request,
    produto_id: int,
    produto_atualizado: ProdutoUpdate,
    session: Session = Depends(get_session)
):
    return servicoProduto.atualizar_produto(
        produto_id, Produto(**produto_atualizado.model_dump()), session
    )


@router.delete(
    "/{produto_id}",
    status_code=204,
    dependencies=[Depends(exigir_api_key)],
)
@limiter.limit(DELETE_LIMIT)
def deletar_produto(
    request: Request,
    produto_id: int, 
    session: Session = Depends(get_session)
):
    return servicoProduto.deletar_produto(produto_id, session)
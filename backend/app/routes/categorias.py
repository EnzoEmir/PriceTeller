from fastapi import APIRouter, Depends, Request
from sqlmodel import Session
from typing import List

from app.core.database import get_session
from app.core.security import exigir_api_key
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaRead, CategoriaUpdate
from app.services.categoria_service import CategoriaService
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter(prefix="/categorias", tags=["Categorias"])

# Cria um limiter específico para este módulo
limiter = Limiter(key_func=get_remote_address)
servicoCategoria = CategoriaService()

@router.post(
    "/",
    response_model=CategoriaRead,
    status_code=201,
    dependencies=[Depends(exigir_api_key)],
)
@limiter.limit("5/minute")  # Limite mais restritivo para criação
def criar_categoria(
    request: Request,
    categoria: CategoriaCreate,
    session: Session = Depends(get_session)
):
    return servicoCategoria.criar_categoria(Categoria(**categoria.model_dump()), session)

@router.get("/", response_model=List[CategoriaRead])
@limiter.limit("100/minute")  # Limite mais alto para leitura
def listar_categoria(
    request: Request,
    session: Session = Depends(get_session)
):
    return servicoCategoria.listar_categorias(session)

@router.get("/{categoria_id}", response_model=CategoriaRead)
@limiter.limit("60/minute")
def buscar_categoria(
    request: Request,
    categoria_id: int,
    session: Session = Depends(get_session)
):
    return servicoCategoria.buscar_categoria(categoria_id, session)

@router.put(
    "/{categoria_id}",
    response_model=CategoriaRead,
    dependencies=[Depends(exigir_api_key)],
)
@limiter.limit("10/minute")
def atualizar_categoria(
    request: Request,
    categoria_id: int,
    categoria: CategoriaUpdate,
    session: Session = Depends(get_session)
):
    return servicoCategoria.atualizar_categoria(
        categoria_id, Categoria(**categoria.model_dump()), session
    )

@router.delete(
    "/{categoria_id}",
    status_code=204,
    dependencies=[Depends(exigir_api_key)],
)
@limiter.limit("5/minute")
def deletar_categoria(
    request: Request,
    categoria_id: int,
    session: Session = Depends(get_session)
):
    servicoCategoria.deletar_categoria(categoria_id, session)
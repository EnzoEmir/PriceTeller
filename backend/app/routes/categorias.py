"""
Camada controller/routes para categorias
Se precisar escalar, pode separar routes de controller
"""

# task 1: fazer dependency injection em categoria: Categoria
# task 2: fazer tratamento de erro
# task 3: fazer validação de input

from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.core.database import get_session
from app.models.categoria import Categoria
from app.services.categoria_service import CategoriaService

router = APIRouter(prefix="/categorias", tags=["Categorias"])

servicoCategoria = CategoriaService()

@router.post("/", response_model=Categoria, status_code=201)
def criar_categoria(
    categoria: Categoria,
    session: Session = Depends(get_session)
):
    return servicoCategoria.criar_categoria(categoria, session)

@router.get("/", response_model=List[Categoria])
def listar_categoria(
    session: Session = Depends(get_session)
):
    return servicoCategoria.listar_categorias(session)

@router.get("/{categoria_id}", response_model=Categoria)
def buscar_categoria(
    categoria_id: int,
    session: Session = Depends(get_session)
):
    return servicoCategoria.buscar_categoria(categoria_id, session)

@router.put("/{categoria_id}", response_model=Categoria)
def atualizar_categoria(
    categoria_id: int,
    categoria: Categoria,
    session: Session = Depends(get_session)
):
    return servicoCategoria.atualizar_categoria(categoria_id, categoria, session)

@router.delete("/{categoria_id}", status_code=204)
def deletar_categoria(
    categoria_id: int,
    session: Session = Depends(get_session)
):
    servicoCategoria.deletar_categoria(categoria_id, session)
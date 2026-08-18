import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
from sqlmodel import Session

from app.core.config import settings
from app.core.database import criar_tabelas, engine
from app.core.exceptions import registrar_handlers
from app.data.loader import carregar_catalogo, carregar_ofertas
from app.models import Categoria, Produto, Loja, Oferta, Historico
from app.routes import categorias, produtos, lojas, ofertas, historico

# logger do próprio uvicorn: um logger novo não teria handler e a mensagem
# sumiria, e print() com stdout em pipe fica preso no buffer
logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    criar_tabelas()

    with Session(engine) as session:
        logger.info("catálogo carregado: %s", carregar_catalogo(session))
        logger.info("ofertas carregadas: %s", carregar_ofertas(session))

    yield


EM_PRODUCAO = settings.em_producao

app = FastAPI(
    lifespan=lifespan,
    docs_url=None if EM_PRODUCAO else "/docs",
    redoc_url=None if EM_PRODUCAO else "/redoc",
    openapi_url=None if EM_PRODUCAO else "/openapi.json",
)

registrar_handlers(app)

# sem allow_credentials: a montagem vive no localStorage e a escrita é
# autenticada por header fora do navegador, então nenhuma resposta precisa
# carregar cookie. Só o navegador chega aqui, e só com GET.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["GET"],
    allow_headers=["Content-Type"],
)

app.include_router(categorias.router)
app.include_router(produtos.router)
app.include_router(lojas.router)
app.include_router(ofertas.router)
app.include_router(historico.router)


@app.get("/")
def read_root():
    return {
        "name": "Price Teller API",
        "version": "1.0.0",
        "status": "online",
        "description": "API para busca de preços de componentes de computadores",
        "docs": None if EM_PRODUCAO else "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "Price Teller API"
    }

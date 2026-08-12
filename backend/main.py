from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from app.core.config import settings
from app.core.database import criar_tabelas
from app.core.exceptions import registrar_handlers
from app.models import Categoria, Produto, Loja, Oferta, Historico
from app.routes import categorias, produtos, lojas, ofertas, historico


@asynccontextmanager
async def lifespan(app: FastAPI):
    criar_tabelas()
    print("Tabelas criadas/verificadas no banco de dados!")
    yield


app = FastAPI(lifespan=lifespan)

registrar_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
        "environment": settings.environment,
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Price Teller API",
        "environment": settings.environment
    }

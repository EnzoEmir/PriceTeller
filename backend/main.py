from fastapi import FastAPI
from datetime import datetime
from app.core.config import settings
from app.core.database import criar_tabelas
from app.models import Categoria, Produto, Loja, Oferta, Historico
from app.routes import categorias, produtos, lojas, ofertas

app = FastAPI()

app.include_router(categorias.router)
app.include_router(produtos.router)
app.include_router(lojas.router)
app.include_router(ofertas.router)




@app.on_event("startup")
def on_startup():
    criar_tabelas()
    print("Tabelas criadas/verificadas no banco de dados!")

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

from fastapi import FastAPI
from datetime import datetime
from app.core.config import settings

app = FastAPI()

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

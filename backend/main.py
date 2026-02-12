from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "name": "Price Teller API",
        "version": "1.0.0",
        "status": "online",
        "description": "API para busca de preços de componentes de computadores",
        "docs": "/docs",
        "health": "/health"
    }

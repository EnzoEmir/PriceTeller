"""
Modelos do banco de dados.
"""
from app.models.categoria import Categoria
from app.models.produto import Produto
from app.models.loja import Loja
from app.models.oferta import Oferta
from app.models.historico import Historico

__all__ = ["Categoria", "Produto", "Loja", "Oferta", "Historico"]

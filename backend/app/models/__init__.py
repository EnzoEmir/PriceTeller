"""
Modelos do banco de dados.
"""
from app.models.categoria import Categoria
from app.models.produto import Produto
from app.models.loja import Loja
from app.models.oferta import Oferta

__all__ = ["Categoria", "Produto", "Loja", "Oferta"]

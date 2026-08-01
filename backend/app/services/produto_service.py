from typing import Optional

from fastapi import HTTPException
from sqlalchemy import String, and_, cast, func, or_
from sqlmodel import Session, select

from app.models.produto import Produto


def _filtro_texto(termo_busca: str):
    """
    Cada palavra digitada precisa aparecer em algum campo, o que faz
    'ryzen 5700' casar sem exigir que o usuário acerte o nome inteiro.
    """
    condicoes = []

    for palavra in termo_busca.split():
        padrao = f"%{palavra}%"
        condicoes.append(
            or_(
                Produto.marca.ilike(padrao),
                Produto.modelo.ilike(padrao),
                cast(Produto.termos_busca, String).ilike(padrao),
            )
        )

    return and_(*condicoes)


class ProdutoService:
    def criar_produto(self, produto: Produto, session: Session):
        """
        Cria um novo produto no banco de dados.
        
        - **fk_categoria_id**: ID da categoria
        - **marca**: Fabricante (ex: 'Intel', 'NVIDIA', 'AMD')
        - **modelo**: Modelo completo (ex: 'Core i7-13700K', 'RTX 4070 Ti')
        - **specs**: Especificações técnicas (JSON, opcional)
        """
        session.add(produto)
        session.commit()
        session.refresh(produto)
        return produto
    
    def listar_produtos(
        self,
        session: Session,
        page: int = 1,
        limit: int = 20,
        q: Optional[str] = None,
        categoria_id: Optional[int] = None,
    ):
        """
        Retorna uma página de produtos e o total de registros que passam no filtro.

        - **page**: número da página, começando em 1
        - **limit**: quantidade de produtos por página
        - **q**: texto buscado em marca, modelo e termos de busca
        - **categoria_id**: restringe a uma categoria
        """
        statement = select(Produto)

        if q and q.strip():
            statement = statement.where(_filtro_texto(q))

        if categoria_id is not None:
            statement = statement.where(Produto.fk_categoria_id == categoria_id)

        total = session.exec(select(func.count()).select_from(statement.subquery())).one()
        produtos = session.exec(
            statement.order_by(Produto.id).offset((page - 1) * limit).limit(limit)
        ).all()
        return produtos, total
    
    def buscar_produto(self, produto_id: int, session: Session):
        """
        Busca um produto específico por ID.
        
        - **produto_id**: ID do produto
        """
        produto = session.get(Produto, produto_id)
        
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        return produto
    
    def atualizar_produto(
        self,
        produto_id: int,
        produto_atualizado: Produto,
        session: Session
    ):
        """
        Atualiza um produto existente.
        
        - **produto_id**: ID do produto a ser atualizado
        - **fk_categoria_id**: Nova categoria
        - **marca**: Nova marca
        - **modelo**: Novo modelo
        - **ean**: Novo código de barras
        - **termos_busca**: Novos nomes alternativos
        - **specs**: Novas especificações (JSON)
        """
        produto = session.get(Produto, produto_id)
        
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        produto.fk_categoria_id = produto_atualizado.fk_categoria_id
        produto.marca = produto_atualizado.marca
        produto.modelo = produto_atualizado.modelo
        produto.ean = produto_atualizado.ean
        produto.termos_busca = produto_atualizado.termos_busca
        produto.specs = produto_atualizado.specs
        
        session.add(produto)
        session.commit()
        session.refresh(produto)
        return produto
    
    def deletar_produto(self, produto_id: int, session: Session):
        """
        Deleta um produto do banco de dados.
        
        - **produto_id**: ID do produto a ser deletado
        """
        produto = session.get(Produto, produto_id)
        
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        session.delete(produto)
        session.commit()
        return None
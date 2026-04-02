from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.produto import Produto


class ProdutoService:
    def __init__():
        pass

    def criar_produto(produto: Produto, session: Session = Depends(get_session)):
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
    
    def listar_produtos(session: Session = Depends(get_session)):
        """
        Retorna todos os produtos cadastrados.
        """
        statement = select(Produto)
        produtos = session.exec(statement).all()
        return produtos
    
    def buscar_produto(produto_id: int, session: Session = Depends(get_session)):
        """
        Busca um produto específico por ID.
        
        - **produto_id**: ID do produto
        """
        produto = session.get(Produto, produto_id)
        
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        return produto
    
    def atualizar_produto(
        produto_id: int,
        produto_atualizado: Produto,
        session: Session = Depends(get_session)
    ):
        """
        Atualiza um produto existente.
        
        - **produto_id**: ID do produto a ser atualizado
        - **fk_categoria_id**: Nova categoria
        - **marca**: Nova marca
        - **modelo**: Novo modelo
        - **specs**: Novas especificações (JSON)
        """
        produto = session.get(Produto, produto_id)
        
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        produto.fk_categoria_id = produto_atualizado.fk_categoria_id
        produto.marca = produto_atualizado.marca
        produto.modelo = produto_atualizado.modelo
        produto.specs = produto_atualizado.specs
        
        session.add(produto)
        session.commit()
        session.refresh(produto)
        return produto
    
    def deletar_produto(produto_id: int, session: Session = Depends(get_session)):
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
from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.categoria import Categoria


class CategoriaService:
    def criar_categoria(self, categoria: Categoria, session: Session):
        """
        Cria uma nova categoria no banco de dados.
        
        - **nome**: Nome da categoria (ex: 'Processador', 'Placa de Vídeo')
        """
        session.add(categoria)
        session.commit()
        session.refresh(categoria)  
        return categoria
    
    def listar_categorias(self, session: Session):
        """
        Retorna todas as categorias cadastradas.
        """
        statement = select(Categoria)
        categorias = session.exec(statement).all()
        return categorias
    
    def buscar_categoria(self, categoria_id: int, session: Session):
        """
        Busca uma categoria específica por ID.
        
        - **categoria_id**: ID da categoria
        """
        categoria = session.get(Categoria, categoria_id)
        
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        
        return categoria
    
    def atualizar_categoria(
        self,
        categoria_id: int,
        categoria_atualizada: Categoria,
        session: Session
    ):
        """
        Atualiza uma categoria existente.
        
        - **categoria_id**: ID da categoria a ser atualizada
        - **nome**: Novo nome da categoria
        """
        categoria = session.get(Categoria, categoria_id)
        
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        
        categoria.nome = categoria_atualizada.nome
        
        session.add(categoria)
        session.commit()
        session.refresh(categoria)
        return categoria
    
    def deletar_categoria(self, categoria_id: int, session: Session):
        """
        Deleta uma categoria do banco de dados.
        
        - **categoria_id**: ID da categoria a ser deletada
        """
        categoria = session.get(Categoria, categoria_id)
        
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        
        session.delete(categoria)
        session.commit()
        return None

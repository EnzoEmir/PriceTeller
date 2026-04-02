from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.loja import Loja


class LojaService:
    def criar_loja(loja: Loja, session: Session = Depends(get_session)):
        """
        Cria uma nova loja no banco de dados.
        
        - **nome**: Nome da loja (ex: 'Kabum', 'Pichau', 'Terabyte')
        - **url_base**: Domínio principal da loja (ex: 'https://www.kabum.com.br')
        """
        session.add(loja)
        session.commit()
        session.refresh(loja)
        return loja
    
    def listar_lojas(session: Session = Depends(get_session)):
        """
        Retorna todas as lojas cadastradas.
        """
        statement = select(Loja)
        lojas = session.exec(statement).all()
        return lojas
    
    def buscar_loja(loja_id: int, session: Session = Depends(get_session)):
        """
        Busca uma loja específica por ID.
        
        - **loja_id**: ID da loja
        """
        loja = session.get(Loja, loja_id)
        
        if not loja:
            raise HTTPException(status_code=404, detail="Loja não encontrada")
        
        return loja
    
    def atualizar_loja(
        loja_id: int,
        loja_atualizada: Loja,
        session: Session = Depends(get_session)
    ):
        """
        Atualiza uma loja existente.
        
        - **loja_id**: ID da loja a ser atualizada
        - **nome**: Novo nome da loja
        - **url_base**: Nova URL base
        """
        loja = session.get(Loja, loja_id)
        
        if not loja:
            raise HTTPException(status_code=404, detail="Loja não encontrada")
        
        loja.nome = loja_atualizada.nome
        loja.url_base = loja_atualizada.url_base
        
        session.add(loja)
        session.commit()
        session.refresh(loja)
        return loja
    
    def deletar_loja(loja_id: int, session: Session = Depends(get_session)):
        """
        Deleta uma loja do banco de dados.
        
        - **loja_id**: ID da loja a ser deletada
        """
        loja = session.get(Loja, loja_id)
        
        if not loja:
            raise HTTPException(status_code=404, detail="Loja não encontrada")
        
        session.delete(loja)
        session.commit()
        return None


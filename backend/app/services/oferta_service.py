from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.oferta import Oferta


class OfertaService:
    def __init__():
        pass

    def criar_oferta(oferta: Oferta, session: Session = Depends(get_session)):
        """
        Cria uma nova oferta no banco de dados.
        
        - **fk_produto_id**: ID do produto
        - **fk_loja_id**: ID da loja
        - **preco_atual**: Preço atual do produto (use string: "1299.90")
        - **url_link**: Link direto para o produto na loja
        """
        session.add(oferta)
        session.commit()
        session.refresh(oferta)
        return oferta
    
    def listar_ofertas(session: Session = Depends(get_session)):
        """
        Retorna todas as ofertas cadastradas.
        """
        statement = select(Oferta)
        ofertas = session.exec(statement).all()
        return ofertas
    
    def buscar_oferta(oferta_id: int, session: Session = Depends(get_session)):
        """
        Busca uma oferta específica por ID.
        
        - **oferta_id**: ID da oferta
        """
        oferta = session.get(Oferta, oferta_id)
        
        if not oferta:
            raise HTTPException(status_code=404, detail="Oferta não encontrada")
        
        return oferta
    
    def atualizar_oferta(
        oferta_id: int,
        oferta_atualizada: Oferta,
        session: Session = Depends(get_session)
    ):
        """
        Atualiza uma oferta existente.
        
        - **oferta_id**: ID da oferta a ser atualizada
        - **fk_produto_id**: Novo produto
        - **fk_loja_id**: Nova loja
        - **preco_atual**: Novo preço
        - **url_link**: Novo link
        """
        oferta = session.get(Oferta, oferta_id)
        
        if not oferta:
            raise HTTPException(status_code=404, detail="Oferta não encontrada")
        
        oferta.fk_produto_id = oferta_atualizada.fk_produto_id
        oferta.fk_loja_id = oferta_atualizada.fk_loja_id
        oferta.preco_atual = oferta_atualizada.preco_atual
        oferta.url_link = oferta_atualizada.url_link
        
        session.add(oferta)
        session.commit()
        session.refresh(oferta)
        return oferta
    
    def deletar_oferta(oferta_id: int, session: Session = Depends(get_session)):
        """
        Deleta uma oferta do banco de dados.
        
        - **oferta_id**: ID da oferta a ser deletada
        """
        oferta = session.get(Oferta, oferta_id)
        
        if not oferta:
            raise HTTPException(status_code=404, detail="Oferta não encontrada")
        
        session.delete(oferta)
        session.commit()
        return None
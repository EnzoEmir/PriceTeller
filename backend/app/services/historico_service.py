from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.historico import Historico

class HistoricoService:
    def __init__():
        pass

    def criar_historico(historico: Historico, session: Session = Depends(get_session)):
        """
        Cria um novo registro de histórico de preço.
        
        - **fk_oferta_id**: ID da oferta monitorada
        - **preco**: Preço registrado (use string: "1299.90")
        - **data**: Data/hora do registro (opcional, preenchido automaticamente se omitido)
        """
        session.add(historico)
        session.commit()
        session.refresh(historico)
        return historico
    
    def listar_historico(session: Session = Depends(get_session)):
        """
        Retorna todos os registros de histórico.
        """
        statement = select(Historico)
        historicos = session.exec(statement).all()
        return historicos
    
    def buscar_historico(historico_id: int, session: Session = Depends(get_session)):
        """
        Busca um registro de histórico específico por ID.
        
        - **historico_id**: ID do registro
        """
        historico = session.get(Historico, historico_id)
        
        if not historico:
            raise HTTPException(status_code=404, detail="Registro de histórico não encontrado")
        
        return historico
    
    def atualizar_historico(
        historico_id: int,
        historico_atualizado: Historico,
        session: Session = Depends(get_session)
    ):
        """
        Atualiza um registro de histórico existente.
        
        - **historico_id**: ID do registro a ser atualizado
        - **fk_oferta_id**: Nova oferta
        - **preco**: Novo preço
        - **data**: Nova data/hora
        """
        historico = session.get(Historico, historico_id)
        
        if not historico:
            raise HTTPException(status_code=404, detail="Registro de histórico não encontrado")
        
        historico.fk_oferta_id = historico_atualizado.fk_oferta_id
        historico.preco = historico_atualizado.preco
        historico.data = historico_atualizado.data
        
        session.add(historico)
        session.commit()
        session.refresh(historico)
        return historico
    
    def deletar_historico(historico_id: int, session: Session = Depends(get_session)):
        """
        Deleta um registro de histórico do banco de dados.
        
        - **historico_id**: ID do registro a ser deletado
        """
        historico = session.get(Historico, historico_id)
        
        if not historico:
            raise HTTPException(status_code=404, detail="Registro de histórico não encontrado")
        
        session.delete(historico)
        session.commit()
        return None

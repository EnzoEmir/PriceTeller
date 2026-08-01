from typing import Sequence

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.loja import Loja
from app.models.oferta import Oferta
from app.schemas.oferta import MelhorOferta, ResumoOfertas


class OfertaService:
    def resumo_por_produto(
        self, session: Session, produto_ids: Sequence[int]
    ) -> dict[int, ResumoOfertas]:
        """
        Menor preço e quantidade de ofertas de cada produto informado.

        Busca tudo numa query só para a listagem não disparar uma consulta por produto.
        """
        if not produto_ids:
            return {}

        linhas = session.exec(
            select(Oferta, Loja.nome)
            .join(Loja, Loja.id == Oferta.fk_loja_id)
            .where(Oferta.fk_produto_id.in_(produto_ids))
        ).all()

        resumos: dict[int, ResumoOfertas] = {}

        for oferta, loja_nome in linhas:
            resumo = resumos.setdefault(oferta.fk_produto_id, ResumoOfertas())
            resumo.total_ofertas += 1

            if resumo.melhor_oferta is None or oferta.preco_atual < resumo.melhor_oferta.preco:
                resumo.melhor_oferta = MelhorOferta(
                    loja_id=oferta.fk_loja_id,
                    loja_nome=loja_nome,
                    preco=oferta.preco_atual,
                    url_link=oferta.url_link,
                )

        return resumos
    def criar_oferta(self, oferta: Oferta, session: Session):
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
    
    def listar_ofertas(self, session: Session):
        """
        Retorna todas as ofertas cadastradas.
        """
        statement = select(Oferta)
        ofertas = session.exec(statement).all()
        return ofertas
    
    def buscar_oferta(self, oferta_id: int, session: Session):
        """
        Busca uma oferta específica por ID.
        
        - **oferta_id**: ID da oferta
        """
        oferta = session.get(Oferta, oferta_id)
        
        if not oferta:
            raise HTTPException(status_code=404, detail="Oferta não encontrada")
        
        return oferta
    
    def atualizar_oferta(
        self,
        oferta_id: int,
        oferta_atualizada: Oferta,
        session: Session
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
    
    def deletar_oferta(self, oferta_id: int, session: Session):
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
from decimal import Decimal
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import String, and_, cast, func, or_
from sqlmodel import Session, select

from app.models.oferta import Oferta
from app.models.produto import Produto
from app.schemas.produto import OrdenacaoProduto


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


def _subquery_menor_preco():
    return (
        select(
            Oferta.fk_produto_id.label("produto_id"),
            func.min(Oferta.preco_atual).label("menor_preco"),
        )
        .group_by(Oferta.fk_produto_id)
        .subquery()
    )


def _ordenacao(ordenar: OrdenacaoProduto, menor_preco):
    # produto sem oferta tem menor_preco nulo; o IS NULL joga esses para o fim
    # nas duas direções, em vez de deixar a ordem por conta do banco
    if ordenar == OrdenacaoProduto.menor_preco:
        return [menor_preco.is_(None), menor_preco.asc(), Produto.id]

    if ordenar == OrdenacaoProduto.maior_preco:
        return [menor_preco.is_(None), menor_preco.desc(), Produto.id]

    if ordenar == OrdenacaoProduto.nome:
        return [Produto.marca, Produto.modelo, Produto.id]

    return [Produto.id]


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
        preco_min: Optional[Decimal] = None,
        preco_max: Optional[Decimal] = None,
        ordenar: OrdenacaoProduto = OrdenacaoProduto.padrao,
    ):
        """
        Retorna uma página de produtos e o total de registros que passam no filtro.

        Preço e ordenação usam sempre a oferta mais barata do produto.

        - **page**: número da página, começando em 1
        - **limit**: quantidade de produtos por página
        - **q**: texto buscado em marca, modelo e termos de busca
        - **categoria_id**: restringe a uma categoria
        - **preco_min** / **preco_max**: faixa de preço da oferta mais barata
        - **ordenar**: padrao, menor_preco, maior_preco ou nome
        """
        precos = _subquery_menor_preco()
        menor_preco = precos.c.menor_preco

        statement = select(Produto).outerjoin(precos, precos.c.produto_id == Produto.id)

        if q and q.strip():
            statement = statement.where(_filtro_texto(q))

        if categoria_id is not None:
            statement = statement.where(Produto.fk_categoria_id == categoria_id)

        if preco_min is not None:
            statement = statement.where(menor_preco >= preco_min)

        if preco_max is not None:
            statement = statement.where(menor_preco <= preco_max)

        total = session.exec(select(func.count()).select_from(statement.subquery())).one()
        produtos = session.exec(
            statement.order_by(*_ordenacao(ordenar, menor_preco))
            .offset((page - 1) * limit)
            .limit(limit)
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
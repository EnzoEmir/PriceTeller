from sqlmodel import Session, select

from app.models.categoria import Categoria
from app.models.loja import Loja
from app.models.produto import Produto
from app.models.oferta import Oferta
from app.models.historico import Historico
from app.services.categoria_service import CategoriaService
from app.services.loja_service import LojaService
from app.services.produto_service import ProdutoService
from app.services.oferta_service import OfertaService
from app.services.historico_service import HistoricoService

from .client import LomadeeClient
from .mapper import extrair_preco, extrair_marca_modelo


class ImportadorLomadee:
    def __init__(self, session: Session, client: LomadeeClient | None = None):
        self.session = session
        self.client = client or LomadeeClient()
        self.categoria_service = CategoriaService()
        self.loja_service = LojaService()
        self.produto_service = ProdutoService()
        self.oferta_service = OfertaService()
        self.historico_service = HistoricoService()
        self._lojas_cache: dict[str, Loja] = {}

    def _get_or_create_categoria(self, nome: str) -> Categoria:
        categoria = self.session.exec(select(Categoria).where(Categoria.nome == nome)).first()
        if categoria:
            return categoria
        return self.categoria_service.criar_categoria(Categoria(nome=nome), self.session)

    def _resolver_loja(self, organization_id: str) -> Loja:
        if organization_id in self._lojas_cache:
            return self._lojas_cache[organization_id]

        marca = self.client.buscar_marca(organization_id)
        nome = marca.get("name") or f"Lomadee #{organization_id}"

        loja = self.session.exec(select(Loja).where(Loja.nome == nome)).first()
        if loja is None:
            loja = self.loja_service.criar_loja(
                Loja(nome=nome, url_base=marca.get("site") or ""),
                self.session,
            )

        self._lojas_cache[organization_id] = loja
        return loja

    def importar(self, query: str, categoria_nome: str, limit: int = 10) -> dict:
        resumo = {"criados": 0, "atualizados": 0, "sem_alteracao": 0, "pulados": 0}
        categoria = self._get_or_create_categoria(categoria_nome)

        for item in self.client.buscar_produtos(query, limit=limit):
            try:
                loja = self._resolver_loja(item["organizationId"])
                marca, modelo = extrair_marca_modelo(item)
                preco = extrair_preco(item)
                url_link = item["url"]
            except (KeyError, TypeError, ValueError) as erro:
                print(f"[lomadee] pulando item sem dado suficiente: {erro}")
                resumo["pulados"] += 1
                continue

            oferta_existente = self.session.exec(
                select(Oferta).where(Oferta.url_link == url_link)
            ).first()

            if oferta_existente is None:
                produto = self.produto_service.criar_produto(
                    Produto(fk_categoria_id=categoria.id, marca=marca, modelo=modelo),
                    self.session,
                )
                self.oferta_service.criar_oferta(
                    Oferta(
                        fk_produto_id=produto.id,
                        fk_loja_id=loja.id,
                        preco_atual=preco,
                        url_link=url_link,
                    ),
                    self.session,
                )
                resumo["criados"] += 1
            elif oferta_existente.preco_atual != preco:
                self.historico_service.criar_historico(
                    Historico(fk_oferta_id=oferta_existente.id, preco=oferta_existente.preco_atual),
                    self.session,
                )
                oferta_existente.preco_atual = preco
                self.session.add(oferta_existente)
                self.session.commit()
                resumo["atualizados"] += 1
            else:
                resumo["sem_alteracao"] += 1

        return resumo

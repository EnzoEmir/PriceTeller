import json
from pathlib import Path
from urllib.parse import urlsplit

from pydantic import ValidationError
from sqlmodel import Session, select

from app.models.categoria import Categoria
from app.models.loja import Loja
from app.models.oferta import Oferta
from app.models.produto import Produto
from app.schemas.categoria import CategoriaCreate
from app.schemas.loja import LojaCreate
from app.schemas.oferta import OfertaCreate
from app.schemas.produto import ProdutoCreate
from app.schemas.tipos import somente_http

CAMINHO_PADRAO = Path(__file__).parent / "catalogo.json"

CAMPOS_PRODUTO = ("fk_categoria_id", "marca", "modelo", "ean", "termos_busca", "specs")
CAMPOS_OFERTA = ("preco_atual", "url_link")


def _ler(caminho: Path) -> dict:
    return json.loads(caminho.read_text(encoding="utf-8"))


def _validar(schema, valores: dict, contexto: str) -> dict:
    """
    Os modelos são `table=True`, e o SQLModel ignora validação nesses, então o
    catálogo entraria no banco sem checagem nenhuma. O erro do Pydantic sozinho
    não diz de qual linha do JSON veio, daí o contexto.
    """
    try:
        return schema(**valores).model_dump()
    except ValidationError as erro:
        raise ValueError(f"{contexto}: {erro}") from erro


def _resolver_por_nome(session: Session, modelo, registros: dict[str, dict]) -> tuple[dict, int]:
    """Cria o que ainda não existe e devolve todos indexados por nome."""
    existentes = {obj.nome: obj for obj in session.exec(select(modelo)).all()}
    criados = 0

    for nome, extras in registros.items():
        if nome not in existentes:
            existentes[nome] = modelo(nome=nome, **extras)
            session.add(existentes[nome])
            criados += 1

    session.commit()
    return existentes, criados


def _sincronizar(destino, valores: dict, campos: tuple[str, ...]) -> bool:
    """Copia os campos que mudaram e diz se algo mudou."""
    if all(getattr(destino, campo) == valores[campo] for campo in campos):
        return False

    for campo in campos:
        setattr(destino, campo, valores[campo])

    return True


class _IndiceProdutos:
    """
    EAN é a chave natural; marca+modelo é o fallback para produto que o
    fornecedor não catalogou. Carrega tudo de uma vez para o loader não
    disparar uma consulta por linha do JSON.
    """

    def __init__(self, session: Session):
        self.por_ean: dict[str, Produto] = {}
        self.por_nome: dict[tuple[str, str], Produto] = {}

        for produto in session.exec(select(Produto)).all():
            self.registrar(produto)

    def registrar(self, produto: Produto) -> None:
        if produto.ean:
            self.por_ean[produto.ean] = produto
        self.por_nome[(produto.marca, produto.modelo)] = produto

    def localizar(self, item: dict) -> Produto | None:
        if item.get("ean") and item["ean"] in self.por_ean:
            return self.por_ean[item["ean"]]
        return self.por_nome.get((item["marca"], item["modelo"]))


def carregar_catalogo(session: Session, caminho: Path = CAMINHO_PADRAO) -> dict:
    dados = _ler(caminho)

    for nome in dados["categorias"]:
        _validar(CategoriaCreate, {"nome": nome}, f"categoria '{nome}'")

    categorias, categorias_criadas = _resolver_por_nome(
        session, Categoria, {nome: {} for nome in dados["categorias"]}
    )
    indice = _IndiceProdutos(session)

    resumo = {
        "categorias_criadas": categorias_criadas,
        "produtos_criados": 0,
        "produtos_atualizados": 0,
        "sem_alteracao": 0,
    }

    for item in dados["produtos"]:
        if item["categoria"] not in categorias:
            raise ValueError(
                f"produto '{item['modelo']}' aponta para categoria fora da lista: "
                f"'{item['categoria']}'"
            )

        valores = _validar(
            ProdutoCreate,
            {
                "fk_categoria_id": categorias[item["categoria"]].id,
                "marca": item["marca"],
                "modelo": item["modelo"],
                "ean": item.get("ean"),
                "termos_busca": item.get("termos_busca"),
                "specs": item.get("specs"),
            },
            f"produto '{item['marca']} {item['modelo']}'",
        )

        produto = indice.localizar(item)

        if produto is None:
            produto = Produto(**valores)
            session.add(produto)
            indice.registrar(produto)
            resumo["produtos_criados"] += 1
        elif _sincronizar(produto, valores, CAMPOS_PRODUTO):
            session.add(produto)
            resumo["produtos_atualizados"] += 1
        else:
            resumo["sem_alteracao"] += 1

    session.commit()
    return resumo


def carregar_ofertas(session: Session, caminho: Path = CAMINHO_PADRAO) -> dict:
    """
    Preço e link de cada produto em cada loja. Roda depois de `carregar_catalogo`,
    porque casa a oferta com o produto que ele já gravou.
    """
    dados = _ler(caminho)

    # a url_base sai do domínio do primeiro anúncio daquela loja
    bases: dict[str, dict] = {}
    for item in dados["produtos"]:
        for oferta in item.get("ofertas", []):
            contexto = f"oferta de '{item['marca']} {item['modelo']}' na loja '{oferta['loja']}'"

            try:
                somente_http(oferta["url_link"])
            except Exception as erro:
                raise ValueError(f"{contexto}: url_link inválido") from erro

            partes = urlsplit(oferta["url_link"])
            loja = _validar(
                LojaCreate,
                {"nome": oferta["loja"], "url_base": f"{partes.scheme}://{partes.netloc}"},
                contexto,
            )
            bases.setdefault(loja["nome"], {"url_base": loja["url_base"]})

    lojas, lojas_criadas = _resolver_por_nome(session, Loja, bases)
    indice = _IndiceProdutos(session)
    existentes = {
        (oferta.fk_produto_id, oferta.fk_loja_id): oferta
        for oferta in session.exec(select(Oferta)).all()
    }

    resumo = {
        "lojas_criadas": lojas_criadas,
        "ofertas_criadas": 0,
        "ofertas_atualizadas": 0,
        "sem_alteracao": 0,
    }

    for item in dados["produtos"]:
        if not item.get("ofertas"):
            continue

        produto = indice.localizar(item)
        if produto is None:
            raise ValueError(
                f"oferta aponta para produto que não está no catálogo: "
                f"'{item['marca']} {item['modelo']}'"
            )

        for dados_oferta in item["ofertas"]:
            loja = lojas[dados_oferta["loja"]]
            valores = _validar(
                OfertaCreate,
                {
                    "fk_produto_id": produto.id,
                    "fk_loja_id": loja.id,
                    "preco_atual": dados_oferta["preco"],
                    "url_link": dados_oferta["url_link"],
                },
                f"oferta de '{item['marca']} {item['modelo']}' na loja '{dados_oferta['loja']}'",
            )

            oferta = existentes.get((produto.id, loja.id))

            if oferta is None:
                session.add(Oferta(**valores))
                resumo["ofertas_criadas"] += 1
            elif _sincronizar(oferta, valores, CAMPOS_OFERTA):
                session.add(oferta)
                resumo["ofertas_atualizadas"] += 1
            else:
                resumo["sem_alteracao"] += 1

    session.commit()
    return resumo


def main():
    from app.core.database import engine, criar_tabelas

    criar_tabelas()
    with Session(engine) as session:
        print(carregar_catalogo(session))
        print(carregar_ofertas(session))


if __name__ == "__main__":
    main()

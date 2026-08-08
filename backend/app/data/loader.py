import json
from pathlib import Path

from sqlmodel import Session, select

from app.models.categoria import Categoria
from app.models.produto import Produto

CAMINHO_PADRAO = Path(__file__).parent / "catalogo.json"

CAMPOS_SINCRONIZADOS = ("fk_categoria_id", "marca", "modelo", "ean", "termos_busca", "specs")


def _resolver_categorias(session: Session, nomes: list[str]) -> tuple[dict[str, Categoria], int]:
    categorias = {}
    criadas = 0

    for nome in nomes:
        categoria = session.exec(select(Categoria).where(Categoria.nome == nome)).first()
        if categoria is None:
            categoria = Categoria(nome=nome)
            session.add(categoria)
            criadas += 1
        categorias[nome] = categoria

    session.commit()
    return categorias, criadas


def _localizar_produto(session: Session, item: dict) -> Produto | None:
    # EAN é a chave natural; marca+modelo é o fallback para produto que o fornecedor não catalogou
    if item.get("ean"):
        produto = session.exec(select(Produto).where(Produto.ean == item["ean"])).first()
        if produto:
            return produto

    return session.exec(
        select(Produto).where(Produto.marca == item["marca"], Produto.modelo == item["modelo"])
    ).first()


def carregar_catalogo(session: Session, caminho: Path = CAMINHO_PADRAO) -> dict:
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    categorias, categorias_criadas = _resolver_categorias(session, dados["categorias"])

    resumo = {
        "categorias_criadas": categorias_criadas,
        "produtos_criados": 0,
        "produtos_atualizados": 0,
        "sem_alteracao": 0,
    }

    for item in dados["produtos"]:
        nome_categoria = item["categoria"]
        if nome_categoria not in categorias:
            raise ValueError(
                f"produto '{item['modelo']}' aponta para categoria fora da lista: '{nome_categoria}'"
            )

        valores = {
            "fk_categoria_id": categorias[nome_categoria].id,
            "marca": item["marca"],
            "modelo": item["modelo"],
            "ean": item.get("ean"),
            "termos_busca": item.get("termos_busca"),
            "specs": item.get("specs"),
        }

        produto = _localizar_produto(session, item)

        if produto is None:
            session.add(Produto(**valores))
            resumo["produtos_criados"] += 1
        elif any(getattr(produto, campo) != valores[campo] for campo in CAMPOS_SINCRONIZADOS):
            for campo in CAMPOS_SINCRONIZADOS:
                setattr(produto, campo, valores[campo])
            session.add(produto)
            resumo["produtos_atualizados"] += 1
        else:
            resumo["sem_alteracao"] += 1

    session.commit()
    return resumo


def main():
    from app.core.database import engine, criar_tabelas

    criar_tabelas()
    with Session(engine) as session:
        print(carregar_catalogo(session))


if __name__ == "__main__":
    main()

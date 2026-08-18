import json

import pytest
from sqlmodel import select

from app.data.loader import CAMINHO_PADRAO, carregar_catalogo, carregar_ofertas
from app.models.oferta import Oferta
from app.models.produto import Produto


class TestCatalogoReal:
    """
    O catalogo.json é carregado no boot e um erro nele derruba a aplicação
    inteira em vez de deixar o site com dado velho. Aqui a falha aparece no CI.
    """

    def test_catalogo_versionado_carrega(self, session):
        resumo = carregar_catalogo(session)

        assert resumo["produtos_criados"] > 0
        assert session.exec(select(Produto)).all()

    def test_ofertas_do_catalogo_carregam(self, session):
        carregar_catalogo(session)
        resumo = carregar_ofertas(session)

        assert resumo["ofertas_criadas"] > 0
        assert session.exec(select(Oferta)).all()

    def test_carregar_duas_vezes_nao_duplica(self, session):
        carregar_catalogo(session)
        carregar_ofertas(session)
        produtos = len(session.exec(select(Produto)).all())
        ofertas = len(session.exec(select(Oferta)).all())

        carregar_catalogo(session)
        carregar_ofertas(session)

        assert len(session.exec(select(Produto)).all()) == produtos
        assert len(session.exec(select(Oferta)).all()) == ofertas


class TestCatalogoInvalido:
    @pytest.fixture
    def escrever(self, tmp_path):
        base = json.loads(CAMINHO_PADRAO.read_text(encoding="utf-8"))

        def _escrever(estragar):
            dados = json.loads(json.dumps(base))
            estragar(dados)
            caminho = tmp_path / "catalogo.json"
            caminho.write_text(json.dumps(dados), encoding="utf-8")
            return caminho

        return _escrever

    @pytest.mark.parametrize(
        "estragar",
        [
            pytest.param(
                lambda d: d["produtos"][0]["ofertas"][0].update({"url_link": "javascript:alert(1)"}),
                id="url_link_nao_http",
            ),
            pytest.param(
                lambda d: d["produtos"][0]["ofertas"][0].update({"preco": "-500.00"}),
                id="preco_negativo",
            ),
            pytest.param(
                lambda d: d["produtos"][0].update({"categoria": "Categoria Inexistente"}),
                id="categoria_fora_da_lista",
            ),
        ],
    )
    def test_recusa_carregar(self, session, escrever, estragar):
        caminho = escrever(estragar)

        with pytest.raises(ValueError):
            carregar_catalogo(session, caminho)
            carregar_ofertas(session, caminho)

import pytest

from app.core.config import settings
from app.models.categoria import Categoria

CHAVE = "chave-de-teste"
HEADER = {"X-API-Key": CHAVE}

URL_BOA = "https://kabum.com.br/produto/1"


@pytest.fixture(autouse=True)
def com_chave_configurada():
    anterior = settings.admin_api_key
    settings.admin_api_key = CHAVE
    yield
    settings.admin_api_key = anterior


@pytest.fixture
def cenario(session):
    categoria = Categoria(nome="Processador")
    session.add(categoria)
    session.commit()
    return categoria


class TestEscritaExigeChave:
    @pytest.mark.parametrize(
        "metodo,rota,corpo",
        [
            ("post", "/categorias/", {"nome": "Nova"}),
            ("put", "/categorias/1", {"nome": "Nova"}),
            ("delete", "/categorias/1", None),
            ("post", "/lojas/", {"nome": "Loja", "url_base": "https://loja.com.br"}),
            ("post", "/ofertas/", {"fk_produto_id": 1, "fk_loja_id": 1, "preco_atual": "10.00", "url_link": URL_BOA}),
        ],
    )
    def test_sem_header_responde_401(self, client, cenario, metodo, rota, corpo):
        resposta = getattr(client, metodo)(rota, json=corpo) if corpo else getattr(client, metodo)(rota)

        assert resposta.status_code == 401

    def test_header_errado_responde_401(self, client, cenario):
        resposta = client.post("/categorias/", json={"nome": "Nova"}, headers={"X-API-Key": "errada"})

        assert resposta.status_code == 401

    def test_com_chave_correta_cria(self, client, cenario):
        resposta = client.post("/categorias/", json={"nome": "Placa de Vídeo"}, headers=HEADER)

        assert resposta.status_code == 201
        assert resposta.json()["nome"] == "Placa de Vídeo"

    def test_sem_chave_configurada_responde_503(self, client, cenario):
        settings.admin_api_key = None

        resposta = client.post("/categorias/", json={"nome": "Nova"}, headers=HEADER)

        assert resposta.status_code == 503

    def test_leitura_continua_publica(self, client, cenario):
        assert client.get("/categorias/").status_code == 200


class TestValidacaoDeEntrada:
    @pytest.mark.parametrize("url", ["javascript:alert(1)", "data:text/html,<script>1</script>", "nao-e-url", ""])
    def test_oferta_recusa_url_fora_de_http(self, client, cenario, url):
        corpo = {"fk_produto_id": 1, "fk_loja_id": 1, "preco_atual": "10.00", "url_link": url}

        assert client.post("/ofertas/", json=corpo, headers=HEADER).status_code == 422

    @pytest.mark.parametrize("preco", ["-1000.00", "-0.01"])
    def test_oferta_recusa_preco_negativo(self, client, cenario, preco):
        corpo = {"fk_produto_id": 1, "fk_loja_id": 1, "preco_atual": preco, "url_link": URL_BOA}

        assert client.post("/ofertas/", json=corpo, headers=HEADER).status_code == 422

    def test_loja_recusa_url_base_fora_de_http(self, client, cenario):
        corpo = {"nome": "Maligna", "url_base": "javascript:alert(1)"}

        assert client.post("/lojas/", json=corpo, headers=HEADER).status_code == 422

    def test_id_enviado_no_corpo_e_ignorado(self, client, cenario, session):
        resposta = client.post("/categorias/", json={"id": 999, "nome": "Injetada"}, headers=HEADER)

        assert resposta.status_code == 201
        assert resposta.json()["id"] != 999
        assert session.get(Categoria, 999) is None

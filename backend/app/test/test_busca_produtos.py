import pytest


def buscar(client, **params):
    resposta = client.get("/produtos/", params=params)
    assert resposta.status_code == 200, resposta.text
    return resposta.json()


def modelos(corpo):
    return [item["modelo"] for item in corpo["items"]]


def precos(corpo):
    return [
        item["melhor_oferta"]["preco"] if item["melhor_oferta"] else None
        for item in corpo["items"]
    ]


class TestPaginacao:
    def test_envelope_traz_metadados(self, client, catalogo):
        corpo = buscar(client)

        assert corpo["total"] == 4
        assert corpo["page"] == 1
        assert corpo["limit"] == 20
        assert corpo["total_pages"] == 1
        assert len(corpo["items"]) == 4

    def test_divide_em_paginas(self, client, catalogo):
        primeira = buscar(client, page=1, limit=3)
        segunda = buscar(client, page=2, limit=3)

        assert primeira["total_pages"] == 2
        assert len(primeira["items"]) == 3
        assert len(segunda["items"]) == 1

    def test_nao_repete_nem_pula_registro(self, client, catalogo):
        vistos = []
        for pagina in (1, 2, 3, 4):
            vistos += [item["id"] for item in buscar(client, page=pagina, limit=1)["items"]]

        assert len(vistos) == 4
        assert len(set(vistos)) == 4

    def test_pagina_alem_do_fim_vem_vazia(self, client, catalogo):
        corpo = buscar(client, page=99)

        assert corpo["items"] == []
        assert corpo["total"] == 4

    @pytest.mark.parametrize("params", [{"page": 0}, {"limit": 0}, {"limit": 101}, {"page": "abc"}])
    def test_rejeita_paginacao_invalida(self, client, catalogo, params):
        assert client.get("/produtos/", params=params).status_code == 422


class TestBuscaPorTexto:
    def test_encontra_pelo_modelo(self, client, catalogo):
        assert modelos(buscar(client, q="ryzen")) == ["Ryzen 7 5700X"]

    def test_ignora_maiusculas(self, client, catalogo):
        assert modelos(buscar(client, q="RYZEN")) == ["Ryzen 7 5700X"]

    def test_encontra_pela_marca(self, client, catalogo):
        assert modelos(buscar(client, q="gigabyte")) == ["GeForce RTX 4060"]

    def test_encontra_por_termo_alternativo(self, client, catalogo):
        # 'R7 5700X' não existe em marca nem modelo, só em termos_busca
        assert modelos(buscar(client, q="R7 5700X")) == ["Ryzen 7 5700X"]

    def test_casa_palavras_em_campos_diferentes(self, client, catalogo):
        # 'amd' está na marca e '5700' no modelo
        assert modelos(buscar(client, q="amd 5700")) == ["Ryzen 7 5700X"]

    def test_casa_palavras_nao_contiguas(self, client, catalogo):
        assert modelos(buscar(client, q="ryzen 5700x")) == ["Ryzen 7 5700X"]

    def test_exige_todas_as_palavras(self, client, catalogo):
        assert buscar(client, q="ryzen gigabyte")["total"] == 0

    def test_sem_resultado(self, client, catalogo):
        assert buscar(client, q="xpto")["total"] == 0

    def test_texto_vazio_nao_filtra(self, client, catalogo):
        assert buscar(client, q="")["total"] == 4
        assert buscar(client, q="   ")["total"] == 4


class TestFiltroPorCategoria:
    def test_restringe_a_categoria(self, client, catalogo):
        corpo = buscar(client, categoria_id=catalogo["categorias"]["processador"])

        assert corpo["total"] == 2
        assert set(modelos(corpo)) == {"Ryzen 7 5700X", "Core i5-13400F"}

    def test_categoria_inexistente_vem_vazia(self, client, catalogo):
        assert buscar(client, categoria_id=999)["total"] == 0

    def test_combina_com_texto(self, client, catalogo):
        corpo = buscar(client, q="core", categoria_id=catalogo["categorias"]["processador"])

        assert modelos(corpo) == ["Core i5-13400F"]


class TestOfertasNaResposta:
    def test_traz_a_oferta_mais_barata(self, client, catalogo):
        item = buscar(client, q="ryzen")["items"][0]

        assert item["total_ofertas"] == 2
        assert item["melhor_oferta"]["preco"] == "850.00"
        assert item["melhor_oferta"]["loja_nome"] == "Pichau"
        assert item["melhor_oferta"]["url_link"] == "https://pichau.com.br/ryzen"

    def test_produto_sem_oferta(self, client, catalogo):
        item = buscar(client, q="sem oferta")["items"][0]

        assert item["total_ofertas"] == 0
        assert item["melhor_oferta"] is None

    def test_uma_consulta_para_todas_as_ofertas(self, client, catalogo, session):
        from sqlalchemy import event

        consultas = []
        engine = session.get_bind()

        def registrar(conn, cursor, statement, *args):
            if statement.strip().upper().startswith("SELECT"):
                consultas.append(statement)

        event.listen(engine, "before_cursor_execute", registrar)
        try:
            buscar(client, limit=100)
        finally:
            event.remove(engine, "before_cursor_execute", registrar)

        # count + produtos + ofertas: não pode crescer com a quantidade de produtos
        assert len(consultas) == 3


class TestFiltroPorPreco:
    def test_preco_maximo(self, client, catalogo):
        assert modelos(buscar(client, preco_max=1000)) == ["Ryzen 7 5700X"]

    def test_preco_minimo(self, client, catalogo):
        corpo = buscar(client, preco_min=1000)

        assert set(modelos(corpo)) == {"Core i5-13400F", "GeForce RTX 4060"}

    def test_faixa(self, client, catalogo):
        assert modelos(buscar(client, preco_min=1000, preco_max=1500)) == ["Core i5-13400F"]

    def test_usa_a_oferta_mais_barata_e_nao_a_mais_cara(self, client, catalogo):
        # a RTX tem oferta de 2000, mas a mais barata é 1900
        assert buscar(client, preco_max=1950)["total"] == 3
        assert "GeForce RTX 4060" in modelos(buscar(client, preco_max=1950))

    def test_exclui_produto_sem_oferta(self, client, catalogo):
        assert "Sem Oferta" not in modelos(buscar(client, preco_min=0))

    def test_faixa_vazia_nao_da_erro(self, client, catalogo):
        assert buscar(client, preco_min=99999)["total"] == 0

    def test_rejeita_preco_negativo(self, client, catalogo):
        assert client.get("/produtos/", params={"preco_min": -5}).status_code == 422


class TestOrdenacao:
    def test_menor_preco(self, client, catalogo):
        assert precos(buscar(client, ordenar="menor_preco")) == ["850.00", "1200.00", "1900.00", None]

    def test_maior_preco(self, client, catalogo):
        assert precos(buscar(client, ordenar="maior_preco")) == ["1900.00", "1200.00", "850.00", None]

    def test_por_nome(self, client, catalogo):
        assert modelos(buscar(client, ordenar="nome")) == [
            "Ryzen 7 5700X",
            "GeForce RTX 4060",
            "Core i5-13400F",
            "Sem Oferta",
        ]

    def test_produto_sem_oferta_fica_por_ultimo_nas_duas_direcoes(self, client, catalogo):
        for ordem in ("menor_preco", "maior_preco"):
            assert modelos(buscar(client, ordenar=ordem))[-1] == "Sem Oferta"

    def test_rejeita_ordenacao_desconhecida(self, client, catalogo):
        assert client.get("/produtos/", params={"ordenar": "xpto"}).status_code == 422


class TestFiltrosCombinados:
    def test_categoria_preco_e_ordenacao(self, client, catalogo):
        corpo = buscar(
            client,
            categoria_id=catalogo["categorias"]["processador"],
            preco_max=1500,
            ordenar="maior_preco",
        )

        assert modelos(corpo) == ["Core i5-13400F", "Ryzen 7 5700X"]

    def test_filtro_reflete_no_total_da_paginacao(self, client, catalogo):
        corpo = buscar(client, categoria_id=catalogo["categorias"]["processador"], limit=1)

        assert corpo["total"] == 2
        assert corpo["total_pages"] == 2
        assert len(corpo["items"]) == 1

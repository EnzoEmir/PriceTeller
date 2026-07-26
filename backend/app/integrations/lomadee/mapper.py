from decimal import Decimal


def extrair_preco(produto: dict) -> Decimal:
    preco_centavos = produto["price"]
    if preco_centavos is None:
        raise ValueError("produto sem preço")
    return Decimal(preco_centavos) / 100


def extrair_marca_modelo(produto: dict) -> tuple[str, str]:
    nome = produto["name"].strip()
    # Lomadee não expõe marca/modelo estruturados, só o nome completo do produto
    primeira_palavra, _, resto = nome.partition(" ")
    if resto:
        return primeira_palavra, resto
    return "Desconhecido", nome

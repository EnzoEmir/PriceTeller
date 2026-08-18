from decimal import Decimal
from typing import Annotated

from pydantic import AfterValidator, Field, HttpUrl, TypeAdapter

_validador_url = TypeAdapter(HttpUrl)


def somente_http(valor: str) -> str:
    """
    Valida como HttpUrl mas devolve a string original. O tipo precisa continuar
    `str` porque o valor vai para uma coluna de texto, e guardar o original evita
    a normalização do Pydantic, que acrescenta barra no fim de domínio puro.
    """
    _validador_url.validate_python(valor)
    return valor


UrlHttp = Annotated[str, AfterValidator(somente_http)]

Preco = Annotated[Decimal, Field(ge=0, max_digits=10, decimal_places=2)]

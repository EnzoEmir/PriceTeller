from secrets import compare_digest
from typing import Optional

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from app.core.config import settings

NOME_HEADER = "X-API-Key"

api_key_header = APIKeyHeader(name=NOME_HEADER, auto_error=False)


def exigir_api_key(chave: Optional[str] = Security(api_key_header)) -> None:
    """
    Protege as rotas de escrita. Sem ADMIN_API_KEY configurada a escrita fica
    desligada em vez de liberada, porque o default de ENVIRONMENT é
    'development' e um deploy que esqueça a variável deixaria tudo aberto.
    """
    if not settings.admin_api_key:
        raise HTTPException(
            status_code=503,
            detail="Escrita desabilitada: ADMIN_API_KEY não configurada",
        )

    if not compare_digest(chave or "", settings.admin_api_key):
        raise HTTPException(
            status_code=401,
            detail=f"Credencial inválida ou ausente no header {NOME_HEADER}",
        )

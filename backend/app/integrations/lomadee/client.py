import httpx

from app.core.config import settings

BASE_URL = "https://api.lomadee.com.br"


class LomadeeClient:
    def __init__(self, api_key: str | None = None, timeout: float = 10.0):
        chave = api_key or settings.lomadee_api_key
        if not chave:
            raise ValueError("LOMADEE_API_KEY não configurada")

        self._client = httpx.Client(
            base_url=BASE_URL,
            timeout=timeout,
            headers={"x-api-key": chave},
        )

    def buscar_produtos(self, search: str, limit: int = 10, page: int = 1) -> list[dict]:
        response = self._client.get(
            "/affiliate/products",
            params={"search": search, "limit": limit, "page": page},
        )
        response.raise_for_status()
        return response.json().get("data", [])

    def buscar_marca(self, organization_id: str) -> dict:
        response = self._client.get(f"/affiliate/brands/{organization_id}")
        response.raise_for_status()
        # formato de resposta (objeto direto vs {"data": {...}}) não confirmado com a API real ainda
        corpo = response.json()
        return corpo["data"] if "data" in corpo else corpo

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

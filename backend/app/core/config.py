from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, model_validator
from typing import Optional


class Settings(BaseSettings):

    """ Configurações da aplicação carregadas de variáveis de ambiente. """

    # Database
    database_url: str = Field(
        default="sqlite:///./database.db",
        description="Database connection URL"
    )
    sql_echo: bool = Field(
        default=False,
        description="Loga no console o SQL gerado pelo SQLAlchemy"
    )

    # API
    api_host: str = Field(
        default="0.0.0.0",
        description="API host address"
    )
    api_port: int = Field(
        default=8000,
        description="API port"
    )
    cors_origins: list[str] = Field(
        default=["http://localhost:3000"],
        description="Origens autorizadas a chamar a API"
    )

    # Security
    admin_api_key: Optional[str] = Field(
        default=None,
        description="Credencial exigida no header X-API-Key pelas rotas de escrita"
    )

    # Environment
    environment: str = Field(
        default="development",
        description="Application environment (development, production, etc)"
    )

    # Lomadee
    lomadee_api_key: Optional[str] = Field(
        default=None,
        description="x-api-key para a API de afiliados da Lomadee"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def em_producao(self) -> bool:
        return self.environment.lower() == "production"

    @model_validator(mode="after")
    def validar_cors_em_producao(self):
        """
        Erra no boot em vez de deixar o site no ar com CORS aberto demais ou
        quebrado. A comparação de origem no Starlette é string exata, por isso
        barra no fim e esquema errado entram como erro e não como detalhe.
        """
        if not self.em_producao:
            return self

        if not self.cors_origins:
            raise ValueError("CORS_ORIGINS vazia: nenhum site conseguiria consumir a API")

        for origem in self.cors_origins:
            if origem == "*":
                raise ValueError("CORS_ORIGINS com '*': liste o domínio exato do frontend")

            if origem.endswith("/"):
                raise ValueError(
                    f"CORS_ORIGINS com barra no fim ('{origem}'): o navegador envia a "
                    "origem sem barra e a comparação nunca casa"
                )

            if not origem.startswith("https://"):
                raise ValueError(f"CORS_ORIGINS sem https ('{origem}')")

        return self


# Instância global das configurações
settings = Settings()

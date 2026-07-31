from pydantic_settings import BaseSettings
from pydantic import Field
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
    secret_key: str = Field(
        default="dev-only-trocar-em-producao",
        description="Secret key for authentication"
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

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Instância global das configurações
settings = Settings()

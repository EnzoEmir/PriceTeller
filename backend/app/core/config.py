from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    
    """ Configurações da aplicação carregadas de variáveis de ambiente. """
    
    # Database
    database_url: str = Field(
        ..., 
        description="PostgreSQL connection URL"
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
    
    # Security
    secret_key: str = Field(
        ..., 
        description="Secret key for authentication"
    )
    
    # Environment
    environment: str = Field(
        default="development", 
        description="Application environment (development, production, etc)"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Instância global das configurações
settings = Settings()

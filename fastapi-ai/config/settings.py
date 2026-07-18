from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Single validated source for every environment variable this service reads.

    Field names map to env vars case-insensitively (chroma_host -> CHROMA_HOST),
    matching the existing docker-compose.yml environment block.
    """

    model_config = SettingsConfigDict(case_sensitive=False)

    chroma_host: str = "chroma-db"
    chroma_port: int = 8000
    chroma_collection_name: str = "portfolio_projects"

    embedding_model: str = "BAAI/bge-small-en-v1.5"

    ollama_base_url: str = "http://host.docker.internal:11434"
    ollama_model: str = "qwen2.5-coder:7b"

    cors_allowed_origins: str = "http://localhost:3000"

    log_level: str = "INFO"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

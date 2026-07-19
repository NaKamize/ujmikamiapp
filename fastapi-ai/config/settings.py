from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Single validated source for every environment variable this service reads.

    Field names map to env vars case-insensitively (chroma_host -> CHROMA_HOST),
    matching the existing docker-compose.yml environment block.
    """

    model_config = SettingsConfigDict(case_sensitive=False)

    chroma_mode: str = "http"
    chroma_host: str = "chroma-db"
    chroma_port: int = 8000
    chroma_ssl: bool = False
    chroma_collection_name: str = "portfolio_projects"

    embedding_model: str = "BAAI/bge-small-en-v1.5"

    # Local provider for LLMs. Ollama is the default
    llm_provider: str = "ollama"

    ollama_base_url: str = "http://host.docker.internal:11434"
    ollama_model: str = "qwen2.5-coder:7b"

    # Only read when llm_provider == "azure_openai".
    azure_openai_endpoint: str = ""
    azure_openai_api_key: str = ""
    azure_openai_deployment: str = "gpt-5.4-mini"
    azure_openai_api_version: str = "2025-04-01-preview"

    cors_allowed_origins: str = "http://localhost:3000"

    log_level: str = "INFO"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

from functools import lru_cache

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "DocuMind AI Service"
    app_version: str = "0.1.0"
    host: str = "0.0.0.0"
    port: int = 8000
    allowed_origins: str = "http://localhost:5173,http://localhost:3000,http://localhost:4000"
    llm_api_key: SecretStr = SecretStr("")
    llm_model: str = ""
    llm_base_url: str = "https://api.openai.com/v1"
    embedding_model: str = ""
    storage_dir: str = "storage"

    @field_validator("llm_base_url", mode="before")
    @classmethod
    def _empty_base_url_falls_back_to_default(cls, value: object) -> object:
        if isinstance(value, str) and not value.strip():
            return "https://api.openai.com/v1"
        return value

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

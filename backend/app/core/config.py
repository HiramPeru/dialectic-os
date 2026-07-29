from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    DATABASE_URL: str = "postgresql://dialectic:dialectic@localhost:5432/dialectic"
    REDIS_URL: str = "redis://localhost:6379/0"
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    LLM_PROVIDER: Literal["nvidia", "deepseek"] = "nvidia"
    LLM_MODEL: str | None = None
    LLM_TIMEOUT_SECONDS: float = 180.0
    LLM_MAX_TOKENS: int = 4096
    NVIDIA_API_KEY: str | None = None
    DEEPSEEK_API_KEY: str | None = None

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip().rstrip("/")
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]

settings = Settings()

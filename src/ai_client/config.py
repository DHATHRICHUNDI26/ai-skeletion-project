
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_base_url: str
    api_key: str
    request_timeout: float = Field(default=10, gt=0)
    max_retries: int = Field(default=3, ge=0)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()

# app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    # App
    app_name: str = "llm-p"
    env: str = "local"

    # JWT
    jwt_secret: str
    jwt_alg: str = "HS256"
    access_token_expire_minutes: int = 60

    # Database
    sqlite_path: str = "./app.db"

    # OpenRouter
    openrouter_api_key: str
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "stepfun/step-3.5-flash:free"
    openrouter_site_url: str = "https://example.com"
    openrouter_app_name: str = "llm-fastapi-openrouter"

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
import os

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Defaults to a local SQLite file so the demo runs with zero setup.
    # Point this at Postgres (see .env.example) for anything beyond a demo.
    database_url: str = "sqlite:///./saarthi_demo.db"
    llm_api_key: str = ""
    llm_model: str = Field(
        default_factory=lambda: os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
        validation_alias="ANTHROPIC_MODEL",
    )
    secret_key: str = "change-me"
    cors_origins: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()

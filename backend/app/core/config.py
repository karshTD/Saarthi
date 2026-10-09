from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"), env_file_encoding="utf-8", extra="ignore"
    )

    # SQLite by default so the demo runs with zero setup; use Postgres in production.
    database_url: str = "sqlite:///./saarthi_demo.db"

    # AI: with no key the app uses deterministic templates (labelled generated_by="template").
    llm_api_key: str = ""
    llm_model: str = "claude-sonnet-5-5"

    # Shared access code required in the X-Access-Code header. Empty = gate disabled (local dev).
    access_code: str = ""

    cors_origins: str = "http://localhost:3000"

    # Max AI-backed requests per client IP per minute. 0 disables limiting.
    ai_rate_limit_per_minute: int = 10

    @field_validator("database_url")
    @classmethod
    def _normalize_database_url(cls, v: str) -> str:
        # Managed Postgres providers hand out postgres:// or postgresql:// URLs.
        for prefix in ("postgres://", "postgresql://"):
            if v.startswith(prefix):
                return "postgresql+psycopg2://" + v[len(prefix):]
        return v

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()

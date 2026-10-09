from app.core.config import Settings


def test_postgres_urls_are_normalised():
    for raw in ("postgres://u:p@h:5432/db", "postgresql://u:p@h:5432/db"):
        assert Settings(database_url=raw).database_url == "postgresql+psycopg2://u:p@h:5432/db"


def test_explicit_driver_and_sqlite_urls_are_untouched():
    url = "postgresql+psycopg2://u:p@h/db"
    assert Settings(database_url=url).database_url == url
    assert Settings(database_url="sqlite:///x.db").database_url == "sqlite:///x.db"


def test_llm_model_env_var_is_used(monkeypatch):
    monkeypatch.setenv("LLM_MODEL", "my-model")
    assert Settings().llm_model == "my-model"


def test_default_model_when_unset(monkeypatch):
    monkeypatch.delenv("LLM_MODEL", raising=False)
    assert Settings().llm_model == "claude-sonnet-5-5"


def test_cors_origins_are_split_and_trimmed():
    s = Settings(cors_origins=" https://a.com , http://localhost:3000,, ")
    assert s.cors_origin_list == ["https://a.com", "http://localhost:3000"]

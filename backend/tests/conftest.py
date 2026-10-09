import os
import tempfile

# Must run before the app is imported: tests never touch a real DB, key, or access code.
_TMP = tempfile.mkdtemp(prefix="saarthi-tests-")
os.environ["DATABASE_URL"] = f"sqlite:///{_TMP}/unused.db"
os.environ["LLM_API_KEY"] = ""
os.environ["ACCESS_CODE"] = ""
os.environ["AI_RATE_LIMIT_PER_MINUTE"] = "1000"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

from app.core.config import settings  # noqa: E402
from app.core.security import limiter  # noqa: E402
from app.db.seed import seed  # noqa: E402
from app.db.session import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(autouse=True)
def _isolated_settings(monkeypatch):
    monkeypatch.setattr(settings, "llm_api_key", "")
    monkeypatch.setattr(settings, "access_code", "")
    monkeypatch.setattr(settings, "ai_rate_limit_per_minute", 1000)
    limiter.reset()


@pytest.fixture()
def session_factory():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    yield sessionmaker(bind=engine, autoflush=False)
    engine.dispose()


@pytest.fixture()
def client(session_factory):
    def override_get_db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def seeded(client, session_factory):
    with session_factory() as db:
        seed(db)
    return client


def new_session(client, class_id=1, **overrides) -> dict:
    body = {
        "class_id": class_id,
        "subject": "Mathematics",
        "topic": "Unlike fractions",
        "duration_minutes": 45,
        **overrides,
    }
    resp = client.post("/api/sessions", json=body)
    assert resp.status_code == 201, resp.text
    return resp.json()

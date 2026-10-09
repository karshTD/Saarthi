from app.core.config import settings


def test_health_is_open_even_with_access_code(client, monkeypatch):
    monkeypatch.setattr(settings, "access_code", "secret")
    assert client.get("/api/health").status_code == 200


def test_access_code_gate(seeded, monkeypatch):
    monkeypatch.setattr(settings, "access_code", "secret")
    assert seeded.get("/api/classes").status_code == 401
    assert seeded.get("/api/classes", headers={"X-Access-Code": "wrong"}).status_code == 401
    assert seeded.get("/api/classes", headers={"X-Access-Code": "secret"}).status_code == 200


def test_gate_disabled_when_no_code_configured(seeded):
    assert seeded.get("/api/classes").status_code == 200


def test_ai_endpoints_are_rate_limited(seeded, monkeypatch):
    monkeypatch.setattr(settings, "ai_rate_limit_per_minute", 2)
    codes = [seeded.post("/api/sessions/1/recommendation").status_code for _ in range(3)]
    assert codes == [200, 200, 429]


def test_rate_limit_only_applies_to_ai_endpoints(seeded, monkeypatch):
    monkeypatch.setattr(settings, "ai_rate_limit_per_minute", 1)
    assert all(seeded.get("/api/classes").status_code == 200 for _ in range(5))


def test_rate_limit_is_per_client_ip(seeded, monkeypatch):
    monkeypatch.setattr(settings, "ai_rate_limit_per_minute", 1)
    a = {"X-Forwarded-For": "1.1.1.1"}
    b = {"X-Forwarded-For": "2.2.2.2"}
    assert seeded.post("/api/sessions/1/recommendation", headers=a).status_code == 200
    assert seeded.post("/api/sessions/1/recommendation", headers=a).status_code == 429
    assert seeded.post("/api/sessions/1/recommendation", headers=b).status_code == 200

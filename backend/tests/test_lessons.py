import pytest

from app.ai.lesson_generator import fit_minutes, generate_lesson
from app.core.config import settings
from app.schemas.lesson import LEVELS
from tests.conftest import new_session

GOOD_AI_PLAN = {
    "title": "Fractions",
    "objective": "Add unlike fractions",
    "sections": [
        {"name": "Intro", "minutes": 10, "description": "d"},
        {"name": "Practice", "minutes": 10, "description": "d"},
    ],
    "activities": [
        {"level": level, "title": f"{level} task", "prompt": "Do it.", "answer": "42"}
        for level in LEVELS
    ],
    "materials": ["paper"],
}


@pytest.mark.parametrize("weights,total", [
    ([0.1, 0.25, 0.25, 0.25, 0.1, 0.05], 45), ([0.1, 0.25, 0.25, 0.25, 0.1, 0.05], 10),
    ([0.1, 0.25, 0.25, 0.25, 0.1, 0.05], 180), ([1, 1, 1], 7), ([5], 30), ([3, 1], 2),
])
def test_fit_minutes_sums_exactly_and_is_positive(weights, total):
    out = fit_minutes(weights, total)
    assert sum(out) == total and all(m >= 1 for m in out)


def test_fit_minutes_rejects_impossible_input():
    with pytest.raises(ValueError):
        fit_minutes([1, 1, 1], 2)
    with pytest.raises(ValueError):
        fit_minutes([], 10)


@pytest.mark.parametrize("duration", [10, 30, 45, 90, 180])
def test_template_plan_respects_duration(duration):
    plan = generate_lesson("Mathematics", "Fractions", duration)["plan"]
    assert sum(s.minutes for s in plan.sections) == plan.total_minutes == duration
    assert sorted(a.level for a in plan.activities) == sorted(LEVELS)


def test_generate_creates_three_activities_and_a_plan(client):
    session = new_session(client, class_id=client.post("/api/classes", json={"name": "C"}).json()["id"])
    body = client.post(f"/api/sessions/{session['id']}/generate-lesson").json()
    assert body["generated_by"] == "template" and body["reused"] is False
    assert [a["difficulty_level"] for a in body["activities"]] == list(LEVELS)
    assert all(a["content"]["generated_by"] == "template" for a in body["activities"])
    assert sum(s["minutes"] for s in body["plan"]["sections"]) == 45
    assert client.get(f"/api/sessions/{session['id']}").json()["lesson_plan"] is not None


def test_repeated_generate_does_not_duplicate_activities(seeded):
    session = new_session(seeded)
    first = seeded.post(f"/api/sessions/{session['id']}/generate-lesson").json()
    second = seeded.post(f"/api/sessions/{session['id']}/generate-lesson").json()
    assert second["reused"] is True
    assert [a["id"] for a in second["activities"]] == [a["id"] for a in first["activities"]]
    assert len(seeded.get(f"/api/sessions/{session['id']}/activities").json()) == 3


def test_seeded_session_is_reused_not_regenerated(seeded):
    body = seeded.post("/api/sessions/1/generate-lesson").json()
    assert body["reused"] is True and body["generated_by"] == "seed"
    assert len(body["activities"]) == 3


def test_regenerate_replaces_activities_when_no_data_recorded(seeded):
    session = new_session(seeded)
    seeded.post(f"/api/sessions/{session['id']}/generate-lesson")
    resp = seeded.post(f"/api/sessions/{session['id']}/generate-lesson?regenerate=true")
    assert resp.status_code == 200 and resp.json()["reused"] is False
    assert len(seeded.get(f"/api/sessions/{session['id']}/activities").json()) == 3


def test_regenerate_refused_once_assessments_exist(seeded):
    assert seeded.post("/api/sessions/1/generate-lesson?regenerate=true").status_code == 409
    assert len(seeded.get("/api/sessions/1/activities").json()) == 3


def test_generate_unknown_session_is_404(client):
    assert client.post("/api/sessions/999/generate-lesson").status_code == 404


def test_ai_success_is_validated_and_timed(seeded, monkeypatch):
    import json

    monkeypatch.setattr(settings, "llm_api_key", "test-key")
    monkeypatch.setattr("app.ai.lesson_generator.complete", lambda *a, **k: json.dumps(GOOD_AI_PLAN))
    session = new_session(seeded, duration_minutes=60)
    body = seeded.post(f"/api/sessions/{session['id']}/generate-lesson").json()
    assert body["generated_by"] == "ai" and body["ai_error"] is None
    assert [s["minutes"] for s in body["plan"]["sections"]] == [30, 30]  # rescaled 10+10 -> 60
    assert body["activities"][0]["content"]["generated_by"] == "ai"


def test_ai_tolerates_markdown_fences(seeded, monkeypatch):
    import json

    monkeypatch.setattr(settings, "llm_api_key", "test-key")
    fenced = "Here you go:\n```json\n" + json.dumps(GOOD_AI_PLAN) + "\n```"
    monkeypatch.setattr("app.ai.lesson_generator.complete", lambda *a, **k: fenced)
    session = new_session(seeded)
    assert seeded.post(f"/api/sessions/{session['id']}/generate-lesson").json()["generated_by"] == "ai"


@pytest.mark.parametrize("bad_output", [
    "I cannot help with that",
    '{"sections": [], "activities": []}',
    '{"title":"t","objective":"o","sections":[{"name":"a","minutes":5,"description":"d"}],'
    '"activities":[{"level":"on_track","title":"t","prompt":"p"}]}',
])
def test_bad_ai_output_falls_back_to_template(seeded, monkeypatch, bad_output):
    monkeypatch.setattr(settings, "llm_api_key", "test-key")
    monkeypatch.setattr("app.ai.lesson_generator.complete", lambda *a, **k: bad_output)
    session = new_session(seeded)
    body = seeded.post(f"/api/sessions/{session['id']}/generate-lesson").json()
    assert body["generated_by"] == "template" and body["ai_error"]
    assert len(body["activities"]) == 3


def test_ai_exception_falls_back_without_leaking_details(seeded, monkeypatch):
    def boom(*a, **k):
        raise ConnectionError("key=sk-secret host unreachable")

    monkeypatch.setattr(settings, "llm_api_key", "test-key")
    monkeypatch.setattr("app.ai.lesson_generator.complete", boom)
    session = new_session(seeded)
    body = seeded.post(f"/api/sessions/{session['id']}/generate-lesson").json()
    assert body["generated_by"] == "template"
    assert body["ai_error"] == "ConnectionError" and "sk-secret" not in str(body)


def test_recommendation_template(seeded):
    body = seeded.post("/api/sessions/1/recommendation").json()
    assert body["generated_by"] == "template"
    assert "3 student(s) are ready" in body["recommendation"]
    assert body["analysis"]["level_counts"]["on_track"] == 4


def test_recommendation_ai_and_fallback(seeded, monkeypatch):
    monkeypatch.setattr(settings, "llm_api_key", "test-key")
    monkeypatch.setattr("app.ai.recommender.complete", lambda *a, **k: '{"recommendation": "Revise."}')
    assert seeded.post("/api/sessions/1/recommendation").json()["generated_by"] == "ai"
    monkeypatch.setattr("app.ai.recommender.complete", lambda *a, **k: '{"nope": 1}')
    body = seeded.post("/api/sessions/1/recommendation").json()
    assert body["generated_by"] == "template" and body["ai_error"] == "ValueError"

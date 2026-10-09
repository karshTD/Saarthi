import pytest


def _payload(client, **overrides):
    activity_id = client.get("/api/sessions/1/activities").json()[0]["id"]
    return {"activity_id": activity_id, "student_id": 1, "score": 0.5,
            "time_taken_seconds": 60, **overrides}


def test_create_assessment(seeded):
    resp = seeded.post("/api/assessments", json=_payload(seeded))
    assert resp.status_code == 201
    assert resp.json()["score"] == 0.5


def test_unknown_student_is_404(seeded):
    assert seeded.post("/api/assessments", json=_payload(seeded, student_id=999)).status_code == 404


def test_unknown_activity_is_404(seeded):
    resp = seeded.post("/api/assessments", json=_payload(seeded, activity_id=999))
    assert resp.status_code == 404


def test_student_from_another_class_is_rejected(seeded):
    class_id = seeded.post("/api/classes", json={"name": "Grade 6"}).json()["id"]
    other = seeded.post("/api/students", json={"name": "Zed", "class_id": class_id}).json()
    resp = seeded.post("/api/assessments", json=_payload(seeded, student_id=other["id"]))
    assert resp.status_code == 422


@pytest.mark.parametrize(
    "field,value",
    [("score", 1.01), ("score", -0.1), ("time_taken_seconds", -1),
     ("time_taken_seconds", 999999), ("attempt_count", 0), ("activity_id", 0)],
)
def test_out_of_range_values_are_rejected(seeded, field, value):
    assert seeded.post("/api/assessments", json=_payload(seeded, **{field: value})).status_code == 422


def test_missing_field_is_rejected(seeded):
    body = _payload(seeded)
    del body["score"]
    assert seeded.post("/api/assessments", json=body).status_code == 422

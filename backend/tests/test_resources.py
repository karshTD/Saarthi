import pytest


def test_create_and_list_classes(client):
    created = client.post("/api/classes", json={"name": "  Grade 7  ", "code": "G7", "grade": "7"})
    assert created.status_code == 201 and created.json()["name"] == "Grade 7"
    client.post("/api/students", json={"name": "A", "class_id": created.json()["id"]})
    listing = client.get("/api/classes").json()
    assert listing[0]["student_count"] == 1 and listing[0]["code"] == "G7"


def test_duplicate_class_code_is_409(client):
    client.post("/api/classes", json={"name": "A", "code": "X"})
    assert client.post("/api/classes", json={"name": "B", "code": "X"}).status_code == 409


def test_class_with_unknown_volunteer_is_404(client):
    assert client.post("/api/classes", json={"name": "A", "volunteer_id": 99}).status_code == 404


@pytest.mark.parametrize("body", [{}, {"name": ""}, {"name": "   "}, {"name": "x" * 201}])
def test_invalid_class_is_422(client, body):
    assert client.post("/api/classes", json=body).status_code == 422


def test_create_student(seeded):
    resp = seeded.post("/api/students", json={
        "name": "Zoya", "class_id": 1, "student_code": "S11", "age": 10, "home_language": "hi"})
    assert resp.status_code == 201 and resp.json()["level"] == "unassessed"


def test_student_code_unique_within_class_only(seeded):
    assert seeded.post("/api/students", json={"name": "X", "class_id": 1, "student_code": "S01"}
                       ).status_code == 409
    other = seeded.post("/api/classes", json={"name": "Other"}).json()["id"]
    assert seeded.post("/api/students", json={"name": "X", "class_id": other, "student_code": "S01"}
                       ).status_code == 201


@pytest.mark.parametrize("extra", [{"age": 1}, {"age": 99}, {"level": "genius"}, {"class_id": 0}])
def test_invalid_student_is_422(seeded, extra):
    assert seeded.post("/api/students", json={"name": "A", "class_id": 1, **extra}).status_code == 422


def test_student_in_unknown_class_is_404(client):
    assert client.post("/api/students", json={"name": "A", "class_id": 5}).status_code == 404


def test_create_and_list_sessions(seeded):
    resp = seeded.post("/api/sessions", json={
        "class_id": 1, "subject": "Mathematics", "topic": "Equivalent fractions",
        "duration_minutes": 30, "language": "hi"})
    assert resp.status_code == 201 and resp.json()["status"] == "planned"
    assert len(seeded.get("/api/sessions?class_id=1").json()) == 2
    assert seeded.get("/api/sessions?class_id=2").json() == []
    assert seeded.get("/api/sessions").json()[0]["topic"] == "Equivalent fractions"  # newest first


@pytest.mark.parametrize("extra", [
    {"duration_minutes": 5}, {"duration_minutes": 500}, {"language": "English!"},
    {"topic": ""}, {"class_id": -1},
])
def test_invalid_session_is_422(seeded, extra):
    body = {"class_id": 1, "subject": "Maths", "topic": "Fractions", "duration_minutes": 45, **extra}
    assert seeded.post("/api/sessions", json=body).status_code == 422


def test_session_for_unknown_class_is_404(client):
    body = {"class_id": 9, "subject": "Maths", "topic": "Fractions", "duration_minutes": 45}
    assert client.post("/api/sessions", json=body).status_code == 404


def test_get_unknown_session_is_404(client):
    assert client.get("/api/sessions/9").status_code == 404
    assert client.get("/api/sessions/9/activities").status_code == 404

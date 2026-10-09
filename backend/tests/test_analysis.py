import pytest

from app.db.seed import STUDENTS
from app.services.class_analysis import classify


@pytest.mark.parametrize(
    "score,level",
    [(0.0, "struggling"), (0.64, "struggling"), (0.65, "on_track"), (0.84, "on_track"),
     (0.85, "advanced"), (1.0, "advanced")],
)
def test_classify_boundaries(score, level):
    assert classify(score) == level


def test_seed_levels_match_computed_levels(seeded):
    """The seed's labels and the live analysis must agree (this was a real bug)."""
    students = seeded.get("/api/classes/1/analysis").json()["students"]
    expected = {name: level for name, _, level in STUDENTS}
    assert {s["name"]: s["level"] for s in students} == expected


def test_seed_counts_are_3_4_3(seeded):
    analysis = seeded.get("/api/classes/1/analysis").json()
    assert analysis["level_counts"] == {"struggling": 3, "on_track": 4, "advanced": 3}
    assert analysis["student_count"] == 10


def test_unassessed_student_falls_back_to_label(seeded):
    seeded.post("/api/students", json={"name": "New", "class_id": 1})
    analysis = seeded.get("/api/classes/1/analysis").json()
    new = next(s for s in analysis["students"] if s["name"] == "New")
    assert new["level"] == "unassessed" and new["avg_score"] is None


def test_analysis_unknown_class_is_404(seeded):
    assert seeded.get("/api/classes/999/analysis").status_code == 404


def test_new_assessments_change_the_analysis(seeded):
    before = seeded.get("/api/classes/1/analysis").json()
    aarav = next(s for s in before["students"] if s["name"] == "Aarav")
    assert aarav["level"] == "struggling"
    activity_id = seeded.get("/api/sessions/1/activities").json()[0]["id"]
    for _ in range(4):
        seeded.post("/api/assessments", json={
            "activity_id": activity_id, "student_id": aarav["student_id"],
            "score": 1.0, "time_taken_seconds": 30,
        })
    after = seeded.get("/api/classes/1/analysis").json()
    assert next(s for s in after["students"] if s["name"] == "Aarav")["level"] == "advanced"

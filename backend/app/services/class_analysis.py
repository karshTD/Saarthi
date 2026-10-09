"""
Class analysis: turns raw Assessment rows into a per-student level
classification and class-wide summary. Deliberately simple and explainable
(threshold on average score) rather than a black box — this is the input
every downstream AI step (lesson generation, recommendations) builds on.
"""
from sqlalchemy import func
from sqlalchemy.orm import Session as DBSession

from app.models.core import Student
from app.models.sessions import Assessment

STRUGGLING_MAX = 0.65
ON_TRACK_MAX = 0.85


def classify(avg_score: float) -> str:
    if avg_score < STRUGGLING_MAX:
        return "struggling"
    if avg_score < ON_TRACK_MAX:
        return "on_track"
    return "advanced"


def analyze_class(db: DBSession, class_id: int) -> dict:
    students = db.query(Student).filter(Student.class_id == class_id).all()

    results = []
    counts = {"struggling": 0, "on_track": 0, "advanced": 0}

    for student in students:
        avg = (
            db.query(func.avg(Assessment.score))
            .filter(Assessment.student_id == student.id)
            .scalar()
        )
        avg_score = float(avg) if avg is not None else None
        level = classify(avg_score) if avg_score is not None else student.level or "unassessed"

        if level in counts:
            counts[level] += 1

        results.append(
            {
                "student_id": student.id,
                "name": student.name,
                "avg_score": round(avg_score, 2) if avg_score is not None else None,
                "level": level,
            }
        )

    return {
        "class_id": class_id,
        "student_count": len(students),
        "level_counts": counts,
        "students": results,
    }

"""
Seeds synthetic demo data: one volunteer, one class, 10 students, a completed fractions
session with three differentiated activities, and their assessments.

Scores are chosen so the computed level of every student matches their seeded level label.
Safe to re-run: skips itself if data exists. Run with: python -m app.db.seed
(after `alembic upgrade head`).
"""
import sys
from datetime import date, timedelta

from sqlalchemy import inspect
from sqlalchemy.orm import Session as DBSession

from app.models.core import Class, Student, Volunteer
from app.models.sessions import Activity, Assessment
from app.models.sessions import Session as SessionModel

STUDENTS = [
    ("Aarav", "S01", "struggling"), ("Diya", "S02", "on_track"), ("Vivaan", "S03", "advanced"),
    ("Ananya", "S04", "struggling"), ("Ishaan", "S05", "on_track"), ("Saanvi", "S06", "on_track"),
    ("Reyansh", "S07", "advanced"), ("Myra", "S08", "struggling"), ("Kabir", "S09", "on_track"),
    ("Anika", "S10", "advanced"),
]

ACTIVITIES = [
    ("struggling", "Adding fractions with pictures",
     "Draw 1/4 and 2/4 as bars and count the shaded parts: 1/4 + 2/4 = ?", "3/4"),
    ("on_track", "Adding like fractions", "Solve 3/8 + 2/8 and explain your steps.", "5/8"),
    ("advanced", "Adding and simplifying fractions",
     "Solve 4/6 + 3/6 and write the answer as a mixed number.", "7/6 = 1 1/6"),
]

# (level, student, score, seconds, attempts)
ASSESSMENTS = [
    ("struggling", "Aarav", 0.60, 210, 2), ("struggling", "Ananya", 0.40, 260, 3),
    ("struggling", "Myra", 0.55, 180, 2),
    ("on_track", "Diya", 0.80, 150, 1), ("on_track", "Ishaan", 0.70, 190, 2),
    ("on_track", "Saanvi", 0.80, 140, 1), ("on_track", "Kabir", 0.75, 170, 1),
    ("advanced", "Vivaan", 0.95, 120, 1), ("advanced", "Reyansh", 1.00, 100, 1),
    ("advanced", "Anika", 0.90, 130, 1),
]


def seed(db: DBSession) -> bool:
    """Insert demo data. Returns False (and does nothing) if the database already has data."""
    if db.query(Volunteer).first():
        return False

    volunteer = Volunteer(name="Demo Volunteer", email="volunteer@saarthi.dev")
    db.add(volunteer)
    db.flush()

    klass = Class(code="G5A", name="Grade 5 - Section A", grade="5", volunteer_id=volunteer.id)
    db.add(klass)
    db.flush()

    students = {}
    for name, code, level in STUDENTS:
        student = Student(name=name, student_code=code, class_id=klass.id, level=level)
        db.add(student)
        students[name] = student
    db.flush()

    session = SessionModel(
        code="G5A-001",
        class_id=klass.id,
        subject="Mathematics",
        topic="Fractions - Addition of Like Fractions",
        language="en",
        duration_minutes=45,
        status="completed",
        session_date=date.today() - timedelta(days=7),
        planned_by="seed",
    )
    db.add(session)
    db.flush()

    activities = {}
    for i, (level, title, prompt, answer) in enumerate(ACTIVITIES):
        activity = Activity(
            session_id=session.id,
            title=title,
            difficulty_level=level,
            order_index=i,
            content={
                "level": level, "title": title, "prompt": prompt, "answer": answer,
                "materials": [], "generated_by": "seed",
            },
        )
        db.add(activity)
        activities[level] = activity
    db.flush()

    for level, name, score, seconds, attempts in ASSESSMENTS:
        db.add(Assessment(
            activity_id=activities[level].id, student_id=students[name].id,
            score=score, time_taken_seconds=seconds, attempt_count=attempts,
        ))

    db.commit()
    return True


def main() -> None:
    from app.db.session import SessionLocal, engine

    if "volunteers" not in inspect(engine).get_table_names():
        sys.exit("Tables not found. Run `alembic upgrade head` first.")
    with SessionLocal() as db:
        if seed(db):
            print("Seeded: 1 volunteer, 1 class, 10 students, 1 session, 3 activities, "
                  "10 assessments.")
        else:
            print("Database already has data - skipping seed.")


if __name__ == "__main__":
    main()

"""
Seeds the database with synthetic demo data: one volunteer, one class,
10 students, a completed fractions session with differentiated activities,
and their assessments.

Works against whatever DATABASE_URL is configured (SQLite by default).
Run with: python -m app.db.seed
"""
from app.db.session import SessionLocal, Base, engine
from app.models.core import Volunteer, Class, Student
from app.models.sessions import Session, Activity, Assessment


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(Volunteer).first():
        print("Database already has data — skipping seed. Delete saarthi_demo.db to reset.")
        db.close()
        return

    volunteer = Volunteer(name="Utkarsh Sharma", email="volunteer1@saarthi.dev")
    db.add(volunteer)
    db.flush()

    klass = Class(name="Grade 5 - Section A", volunteer_id=volunteer.id)
    db.add(klass)
    db.flush()

    student_data = [
        ("Aarav", "struggling"), ("Diya", "on_track"), ("Vivaan", "advanced"),
        ("Ananya", "struggling"), ("Ishaan", "on_track"), ("Saanvi", "on_track"),
        ("Reyansh", "advanced"), ("Myra", "struggling"), ("Kabir", "on_track"),
        ("Anika", "advanced"),
    ]
    students = {}
    for name, level in student_data:
        s = Student(name=name, class_id=klass.id, level=level)
        db.add(s)
        db.flush()
        students[name] = s

    session = Session(
        class_id=klass.id,
        subject="Mathematics",
        topic="Fractions - Addition of Like Fractions",
        language="en",
        duration_minutes=45,
        status="completed",
    )
    db.add(session)
    db.flush()

    activities_data = [
        ("Adding fractions with pictures", "struggling",
         {"type": "visual", "question": "1/4 + 2/4 = ?", "answer": "3/4"}),
        ("Adding like fractions", "on_track",
         {"type": "numeric", "question": "3/8 + 2/8 = ?", "answer": "5/8"}),
        ("Adding and simplifying fractions", "advanced",
         {"type": "numeric", "question": "4/6 + 3/6 = ?", "answer": "7/6 = 1 1/6"}),
    ]
    activities = {}
    for i, (title, level, content) in enumerate(activities_data):
        a = Activity(session_id=session.id, title=title, difficulty_level=level, content=content, order_index=i)
        db.add(a)
        db.flush()
        activities[level] = a

    assessment_data = [
        ("struggling", "Aarav", 0.60, 210, 2), ("struggling", "Ananya", 0.40, 260, 3), ("struggling", "Myra", 0.80, 180, 1),
        ("on_track", "Diya", 0.85, 150, 1), ("on_track", "Ishaan", 0.70, 190, 2),
        ("on_track", "Saanvi", 0.90, 140, 1), ("on_track", "Kabir", 0.75, 170, 1),
        ("advanced", "Vivaan", 0.95, 120, 1), ("advanced", "Reyansh", 1.00, 100, 1), ("advanced", "Anika", 0.90, 130, 1),
    ]
    for level, name, score, time_s, attempts in assessment_data:
        db.add(Assessment(
            activity_id=activities[level].id,
            student_id=students[name].id,
            score=score,
            time_taken_seconds=time_s,
            attempt_count=attempts,
        ))

    db.commit()
    db.close()
    print("Seeded: 1 volunteer, 1 class, 10 students, 1 session, 3 activities, 10 assessments.")


if __name__ == "__main__":
    seed()

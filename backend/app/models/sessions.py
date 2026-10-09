from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    false,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class Session(Base):
    """A single class session (one sitting with a group of students)."""

    __tablename__ = "sessions"
    __table_args__ = (UniqueConstraint("code", name="uq_sessions_code"),)

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=True)  # stable id used by CSV import
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    subject = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    language = Column(String, default="en")
    duration_minutes = Column(Integer, nullable=False)
    status = Column(String, default="planned")  # planned / in_progress / completed
    session_date = Column(Date, nullable=True)
    planned_by = Column(String, default="saarthi", server_default="saarthi")
    volunteer_notes = Column(Text, nullable=True)
    lesson_plan = Column(JSON, nullable=True)  # validated LessonPlan, see schemas/lesson.py
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    class_ = relationship("Class")
    activities = relationship(
        "Activity",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="Activity.order_index",
    )


class Activity(Base):
    """One differentiated activity generated for a session, at a given difficulty level."""

    __tablename__ = "activities"
    __table_args__ = (
        UniqueConstraint("session_id", "difficulty_level", name="uq_activity_session_level"),
    )

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    title = Column(String, nullable=False)
    difficulty_level = Column(String, nullable=False)  # struggling / on_track / advanced
    content = Column(JSON, nullable=False)
    order_index = Column(Integer, default=0)

    session = relationship("Session", back_populates="activities")
    assessments = relationship(
        "Assessment", back_populates="activity", cascade="all, delete-orphan"
    )


class Assessment(Base):
    """A single student's summary result on a single activity."""

    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    score = Column(Float, nullable=False)  # 0.0-1.0 normalized correctness
    time_taken_seconds = Column(Integer, nullable=False)
    attempt_count = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    activity = relationship("Activity", back_populates="assessments")
    student = relationship("Student", back_populates="assessments")


class Progress(Base):
    """Rolling per-student, per-topic mastery snapshot, updated after each session."""

    __tablename__ = "progress"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    topic = Column(String, nullable=False)
    mastery_level = Column(String, nullable=False)  # struggling / on_track / advanced
    avg_score = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    student = relationship("Student", back_populates="progress_records")


class Attendance(Base):
    __tablename__ = "attendance"
    __table_args__ = (UniqueConstraint("session_id", "student_id", name="uq_attendance"),)

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    present = Column(Boolean, nullable=False)


class AssessmentItem(Base):
    """One student's answer to one question. Source of truth for onsite-collected data."""

    __tablename__ = "assessment_items"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=True)
    question_text = Column(Text, nullable=False)
    difficulty = Column(String, nullable=True)
    correct = Column(Boolean, nullable=False)
    time_seconds = Column(Integer, nullable=True)
    attempts = Column(Integer, nullable=False, default=1, server_default="1")
    hint_used = Column(Boolean, nullable=False, default=False, server_default=false())
    misconception_tag = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class LessonFeedback(Base):
    __tablename__ = "lesson_feedback"
    __table_args__ = (CheckConstraint("rating BETWEEN 1 AND 5", name="ck_feedback_rating"),)

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    what_worked = Column(Text, nullable=True)
    what_didnt = Column(Text, nullable=True)
    time_overran = Column(Boolean, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

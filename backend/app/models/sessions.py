from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text,
    JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class Session(Base):
    """A single class session (one sitting with a group of students)."""

    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    subject = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    language = Column(String, default="en")
    duration_minutes = Column(Integer, nullable=False)
    status = Column(String, default="planned")  # planned / in_progress / completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    class_ = relationship("Class")
    activities = relationship("Activity", back_populates="session", cascade="all, delete-orphan")


class Activity(Base):
    """One differentiated activity/question generated for a session, at a given difficulty level."""

    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    title = Column(String, nullable=False)
    difficulty_level = Column(String, nullable=False)  # struggling / on_track / advanced
    content = Column(JSON, nullable=False)  # generated question/activity payload
    order_index = Column(Integer, default=0)

    session = relationship("Session", back_populates="activities")
    assessments = relationship("Assessment", back_populates="activity", cascade="all, delete-orphan")


class Assessment(Base):
    """A single student's recorded response to a single activity."""

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
    notes = Column(Text, nullable=True)  # recommendation text for next session
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    student = relationship("Student", back_populates="progress_records")

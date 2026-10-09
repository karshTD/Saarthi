from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class Volunteer(Base):
    __tablename__ = "volunteers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    classes = relationship("Class", back_populates="volunteer")


class Class(Base):
    __tablename__ = "classes"
    __table_args__ = (UniqueConstraint("code", name="uq_classes_code"),)

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=True)  # short stable id used by CSV import, e.g. "G5A"
    name = Column(String, nullable=False)
    grade = Column(String, nullable=True)
    location = Column(String, nullable=True)
    volunteer_id = Column(Integer, ForeignKey("volunteers.id"))

    volunteer = relationship("Volunteer", back_populates="classes")
    students = relationship("Student", back_populates="class_")


class Student(Base):
    __tablename__ = "students"
    __table_args__ = (UniqueConstraint("class_id", "student_code", name="uq_students_class_code"),)

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # alias / first name only; never a full legal name
    student_code = Column(String, nullable=True)  # pseudonymous code, e.g. "S01"
    class_id = Column(Integer, ForeignKey("classes.id"))
    level = Column(String, default="unassessed")  # struggling / on_track / advanced / unassessed
    age = Column(Integer, nullable=True)
    home_language = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    class_ = relationship("Class", back_populates="students")
    assessments = relationship("Assessment", back_populates="student")
    progress_records = relationship("Progress", back_populates="student")

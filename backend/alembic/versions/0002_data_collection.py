"""data-collection tables and columns, lesson plans, activity uniqueness

Revision ID: 0002_data_collection
Revises: 0001_initial
Create Date: 2026-10-08

"""
import sqlalchemy as sa
from alembic import op

revision = "0002_data_collection"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("classes") as b:
        b.add_column(sa.Column("code", sa.String(), nullable=True))
        b.add_column(sa.Column("grade", sa.String(), nullable=True))
        b.add_column(sa.Column("location", sa.String(), nullable=True))
        b.create_unique_constraint("uq_classes_code", ["code"])

    with op.batch_alter_table("students") as b:
        b.add_column(sa.Column("student_code", sa.String(), nullable=True))
        b.add_column(sa.Column("age", sa.Integer(), nullable=True))
        b.add_column(sa.Column("home_language", sa.String(), nullable=True))
        b.add_column(sa.Column("notes", sa.Text(), nullable=True))
        b.create_unique_constraint("uq_students_class_code", ["class_id", "student_code"])

    with op.batch_alter_table("sessions") as b:
        b.add_column(sa.Column("code", sa.String(), nullable=True))
        b.add_column(sa.Column("session_date", sa.Date(), nullable=True))
        b.add_column(
            sa.Column("planned_by", sa.String(), nullable=True, server_default="saarthi")
        )
        b.add_column(sa.Column("volunteer_notes", sa.Text(), nullable=True))
        b.add_column(sa.Column("lesson_plan", sa.JSON(), nullable=True))
        b.create_unique_constraint("uq_sessions_code", ["code"])

    # The old generate endpoint could insert duplicate activities. Collapse them onto the
    # lowest id per (session, level), moving any assessments across, before enforcing uniqueness.
    op.execute(
        """
        UPDATE assessments SET activity_id = (
            SELECT MIN(a2.id) FROM activities a2
            JOIN activities a1 ON a1.id = assessments.activity_id
            WHERE a2.session_id = a1.session_id AND a2.difficulty_level = a1.difficulty_level
        )
        """
    )
    op.execute(
        "DELETE FROM activities WHERE id NOT IN "
        "(SELECT MIN(id) FROM activities GROUP BY session_id, difficulty_level)"
    )
    with op.batch_alter_table("activities") as b:
        b.create_unique_constraint("uq_activity_session_level", ["session_id", "difficulty_level"])

    op.create_table(
        "attendance",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("session_id", sa.Integer(), sa.ForeignKey("sessions.id"), nullable=False),
        sa.Column("student_id", sa.Integer(), sa.ForeignKey("students.id"), nullable=False),
        sa.Column("present", sa.Boolean(), nullable=False),
        sa.UniqueConstraint("session_id", "student_id", name="uq_attendance"),
    )
    op.create_table(
        "assessment_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("session_id", sa.Integer(), sa.ForeignKey("sessions.id"), nullable=False),
        sa.Column("student_id", sa.Integer(), sa.ForeignKey("students.id"), nullable=False),
        sa.Column("activity_id", sa.Integer(), sa.ForeignKey("activities.id"), nullable=True),
        sa.Column("question_text", sa.Text(), nullable=False),
        sa.Column("difficulty", sa.String(), nullable=True),
        sa.Column("correct", sa.Boolean(), nullable=False),
        sa.Column("time_seconds", sa.Integer(), nullable=True),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("hint_used", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("misconception_tag", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "lesson_feedback",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("session_id", sa.Integer(), sa.ForeignKey("sessions.id"), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("what_worked", sa.Text(), nullable=True),
        sa.Column("what_didnt", sa.Text(), nullable=True),
        sa.Column("time_overran", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.CheckConstraint("rating BETWEEN 1 AND 5", name="ck_feedback_rating"),
    )


def downgrade() -> None:
    op.drop_table("lesson_feedback")
    op.drop_table("assessment_items")
    op.drop_table("attendance")

    with op.batch_alter_table("activities") as b:
        b.drop_constraint("uq_activity_session_level", type_="unique")

    with op.batch_alter_table("sessions") as b:
        b.drop_constraint("uq_sessions_code", type_="unique")
        for col in ("lesson_plan", "volunteer_notes", "planned_by", "session_date", "code"):
            b.drop_column(col)

    with op.batch_alter_table("students") as b:
        b.drop_constraint("uq_students_class_code", type_="unique")
        for col in ("notes", "home_language", "age", "student_code"):
            b.drop_column(col)

    with op.batch_alter_table("classes") as b:
        b.drop_constraint("uq_classes_code", type_="unique")
        for col in ("location", "grade", "code"):
            b.drop_column(col)

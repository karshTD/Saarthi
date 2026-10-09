from pathlib import Path

import pytest
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.migration import MigrationContext
from sqlalchemy import create_engine, inspect, text

from alembic import command
from app.db.session import Base

BACKEND = Path(__file__).resolve().parent.parent


def _config(db_path: Path) -> Config:
    cfg = Config(str(BACKEND / "alembic.ini"))
    cfg.set_main_option("script_location", str(BACKEND / "alembic"))
    cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")
    return cfg


@pytest.fixture()
def db_path(tmp_path):
    return tmp_path / "migrate.db"


def test_models_and_migrations_agree(db_path):
    """Fails if someone edits a model without writing a migration (schema drift)."""
    command.upgrade(_config(db_path), "head")
    engine = create_engine(f"sqlite:///{db_path}")
    with engine.connect() as conn:
        diff = compare_metadata(MigrationContext.configure(conn), Base.metadata)
    assert diff == []


def test_upgrade_downgrade_upgrade(db_path):
    cfg = _config(db_path)
    command.upgrade(cfg, "head")
    command.downgrade(cfg, "0001_initial")
    tables = set(inspect(create_engine(f"sqlite:///{db_path}")).get_table_names())
    assert "attendance" not in tables and "classes" in tables
    command.upgrade(cfg, "head")
    tables = set(inspect(create_engine(f"sqlite:///{db_path}")).get_table_names())
    assert {"attendance", "assessment_items", "lesson_feedback"} <= tables


def test_upgrade_merges_duplicate_activities_and_keeps_assessments(db_path):
    """Databases created before the dedupe fix can hold duplicate activities."""
    cfg = _config(db_path)
    command.upgrade(cfg, "0001_initial")
    engine = create_engine(f"sqlite:///{db_path}")
    with engine.begin() as conn:
        conn.execute(text("INSERT INTO volunteers (id, name, email) VALUES (1, 'v', 'v@x.dev')"))
        conn.execute(text("INSERT INTO classes (id, name, volunteer_id) VALUES (1, 'c', 1)"))
        conn.execute(text("INSERT INTO students (id, name, class_id) VALUES (1, 's', 1)"))
        conn.execute(text("INSERT INTO sessions (id, class_id, subject, topic, duration_minutes) "
                          "VALUES (1, 1, 'm', 't', 45)"))
        for act_id in (1, 2):  # same session + level twice
            conn.execute(text(
                "INSERT INTO activities (id, session_id, title, difficulty_level, content, order_index)"
                f" VALUES ({act_id}, 1, 't', 'on_track', '{{}}', 0)"))
            conn.execute(text(
                "INSERT INTO assessments (activity_id, student_id, score, time_taken_seconds) "
                f"VALUES ({act_id}, 1, 0.5, 10)"))
    command.upgrade(cfg, "head")
    with engine.connect() as conn:
        assert conn.execute(text("SELECT id FROM activities")).scalars().all() == [1]
        assert conn.execute(text("SELECT activity_id FROM assessments")).scalars().all() == [1, 1]

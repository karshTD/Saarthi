# Saarthi Backend

FastAPI backend for Saarthi — class analysis, differentiated lesson
generation, sessions, assessments, and next-session recommendations.

## Stack

- FastAPI + Pydantic v2
- SQLAlchemy + Alembic. SQLite for local demos, Postgres for anything beyond (`DATABASE_URL`)
- Anthropic Claude for lesson/recommendation generation when `LLM_API_KEY` is set, with a
  deterministic template fallback otherwise. Every AI-backed response says which one produced it
  (`generated_by: "ai" | "template" | "seed"`).

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
alembic upgrade head        # create the schema
python -m app.db.seed       # synthetic demo data (safe to re-run)
uvicorn app.main:app --reload
```

No `.env` is required locally. API docs: `http://localhost:8000/docs`.

## Endpoints (all under `/api`; all except `/health` need `X-Access-Code` if `ACCESS_CODE` is set)

| Method | Path | Notes |
|---|---|---|
| GET | `/health` | Open |
| GET / POST | `/classes` | List with student counts / create (201) |
| GET | `/classes/{id}/analysis` | Live level classification (404 if unknown) |
| POST | `/students` | Create (201); `student_code` unique per class (409) |
| GET / POST | `/sessions` | List (`?class_id=`) / create (201) |
| GET | `/sessions/{id}`, `/sessions/{id}/activities` | Session incl. stored lesson plan / activities |
| POST | `/sessions/{id}/generate-lesson` | Idempotent. Returns `reused: true` if a lesson exists. `?regenerate=true` replaces it, refused (409) once assessments exist. Rate limited |
| POST | `/sessions/{id}/recommendation` | Next-session recommendation. Rate limited |
| POST | `/assessments` | Validates student and activity exist and share a class (404/422) |

## Tests and lint

```bash
pytest          # 80+ tests: API, validation, AI fallback (mocked), migrations incl. drift check
ruff check .
```

## Production

`Dockerfile.prod` runs `start.sh`: `alembic upgrade head`, optional seed (`SEED_ON_START=true`),
then uvicorn. See `../DEPLOY.md`.

## Structure

```
app/
|-- api/        route handlers
|-- ai/         llm.py (Anthropic wrapper), lesson_generator.py, recommender.py
|-- core/       config, security (access code + rate limit)
|-- models/     SQLAlchemy models
|-- schemas/    Pydantic schemas (lesson.py is the lesson-plan contract)
|-- services/   class_analysis.py (level classification)
`-- db/         session setup, seed.py
alembic/        migrations
tests/
```

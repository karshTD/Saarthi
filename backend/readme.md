# Saarthi Backend

FastAPI backend for Saarthi — class analysis, differentiated lesson
generation, sessions, assessments, and next-session recommendations.

## Stack

- FastAPI + Pydantic
- SQLAlchemy + Alembic — defaults to a local SQLite file for zero-setup
  demos; point `DATABASE_URL` at Postgres for anything beyond that
- Anthropic Claude for lesson/recommendation generation, with an
  automatic offline template fallback when no API key is configured

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

No `.env` file is required to run the demo — it defaults to SQLite and
falls back to template-based generation with no API key. Copy
`../.env.example` to `../.env` and set `LLM_API_KEY` to switch lesson
generation and recommendations over to real Claude calls.

## Database

```bash
alembic upgrade head        # creates the schema (saarthi_demo.db by default)
python -m app.db.seed       # loads 1 class, 10 students, 1 completed session
```

Re-running the seed script is safe — it skips itself if data already exists.
Delete `saarthi_demo.db` to reset.

## Run

```bash
uvicorn app.main:app --reload
```

API docs: `http://localhost:8000/docs`
Health check: `http://localhost:8000/api/health`

## Key endpoints

- `GET  /api/classes/{id}/analysis` — live level classification from assessment data
- `POST /api/sessions` — create a session
- `POST /api/sessions/{id}/generate-lesson` — generate 3 differentiated activities (AI or template)
- `POST /api/assessments` — record a student's response to an activity
- `POST /api/sessions/{id}/recommendation` — next-session recommendation from current class analysis

Every AI-backed response includes `"generated_by": "ai" | "template"` so
it's always clear which mode produced it — useful to point out live in a
demo.

## Structure

```
app/
├── api/        # route handlers (classes, sessions, assessments, health)
├── ai/         # lesson_generator.py, recommender.py — dual-mode AI/template
├── models/     # SQLAlchemy models
├── schemas/    # Pydantic request/response schemas
├── services/   # class_analysis.py — level classification logic
├── db/         # session setup + seed.py
└── core/       # config, settings
alembic/        # migrations
```

## Tests

```bash
pytest
```

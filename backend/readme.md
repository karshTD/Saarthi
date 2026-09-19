
# Saarthi Backend

FastAPI backend for Saarthi — class analysis, lesson generation, sessions, and progress tracking.

## Stack

- FastAPI + Pydantic
- SQLAlchemy + Alembic (Postgres)
- SentenceTransformers + FAISS (RAG, added in later phases)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example ../.env  # fill in DATABASE_URL, LLM_API_KEY, etc.
```

## Database

Run migrations before starting the API:

```bash
alembic upgrade head
```

Load sample data (one class, 10 students, a fractions session):

```bash
psql $DATABASE_URL -f app/db/seed.sql
```

Create a new migration after changing models:

```bash
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

## Run

```bash
uvicorn app.main:app --reload
```

API docs: `http://localhost:8000/docs`
Health check: `http://localhost:8000/api/health`

## Structure

```
app/
├── api/        # route handlers
├── ai/         # lesson generation, RAG, LLM calls
├── models/     # SQLAlchemy models
├── schemas/    # Pydantic request/response schemas
├── services/   # business logic (class analysis, etc.)
├── db/         # session setup + seed.sql
└── core/       # config, settings
alembic/        # migrations
```

## Tests

```bash
pytest
```

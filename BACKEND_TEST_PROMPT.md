# Backend test brief (paste this into the tool/agent that will test Saarthi's backend)

You are testing the **backend** of Saarthi, a FastAPI + SQLAlchemy + Alembic service that helps NGO
volunteers plan differentiated lessons and track student levels. You have the repo (`backend/`).
Your job: verify it behaves as documented below, try to break it, and report findings. Do not
refactor or add features. Fix nothing unless asked; report.

## 1. Setup (Python 3.11+)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q && ruff check .                 # expect: all tests pass, lint clean
alembic upgrade head && python -m app.db.seed
uvicorn app.main:app --port 8000
```
No `.env` needed. Optional env: `DATABASE_URL`, `LLM_API_KEY`, `LLM_MODEL`, `ACCESS_CODE`,
`CORS_ORIGINS`, `AI_RATE_LIMIT_PER_MINUTE`. Docs at `/docs`. Everything is under `/api`.

## 2. Contract
- `GET /api/health` -> `{"status":"ok",...}`. Always open.
- If `ACCESS_CODE` is set, every other `/api/*` route needs header `X-Access-Code`, else 401.
- `GET/POST /api/classes` (create -> 201; duplicate `code` -> 409; unknown `volunteer_id` -> 404).
- `GET /api/classes/{id}/analysis` -> `level_counts`, per-student `avg_score` and `level`. Unknown class -> 404.
  Levels come from average score: `<0.65` struggling, `<0.85` on_track, else advanced; students with no
  assessments keep their stored label (`unassessed` by default).
- `POST /api/students` (201; `student_code` unique **per class**, duplicate -> 409; age 3-25).
- `POST /api/sessions` (201; `duration_minutes` 10-180; `language` like `en`/`hi`; unknown class -> 404),
  `GET /api/sessions?class_id=`, `GET /api/sessions/{id}`, `GET /api/sessions/{id}/activities`.
- `POST /api/sessions/{id}/generate-lesson`:
  - Creates exactly 3 activities (struggling, on_track, advanced) and a `plan` whose section minutes sum
    to the session duration. `generated_by` is `template` with no key, `ai` with a working key.
  - **Idempotent:** calling again returns the same activities with `reused: true`. Never duplicates.
  - `?regenerate=true` replaces them, but returns 409 if any assessment exists for them.
  - If the AI call fails or returns invalid JSON/shape, it falls back to the template and sets
    `ai_error` to a short class name (never raw exception text or secrets).
- `POST /api/sessions/{id}/recommendation` -> `recommendation`, `generated_by`, `analysis`.
- Both AI endpoints are rate limited per client IP (`AI_RATE_LIMIT_PER_MINUTE`, default 10) -> 429.
- `POST /api/assessments` (201): `score` in [0,1], `time_taken_seconds` 0-7200, `attempt_count` 1-20;
  unknown student/activity -> 404; student from a different class than the activity -> 422.

Seed data (`python -m app.db.seed`): class 1 "Grade 5 - Section A", 10 students, session 1 with 3
activities and 10 assessments. Expected analysis counts: struggling 3, on_track 4, advanced 3, and each
student's computed level equals their seeded label.

## 3. Quick manual script
```bash
B=http://localhost:8000/api
curl -s $B/classes/1/analysis | python -m json.tool | head -20
SID=$(curl -s -XPOST $B/sessions -H 'content-type: application/json' \
  -d '{"class_id":1,"subject":"Mathematics","topic":"Unlike fractions","duration_minutes":45}' | python -c 'import sys,json;print(json.load(sys.stdin)["id"])')
curl -s -XPOST $B/sessions/$SID/generate-lesson | python -m json.tool | head -40
curl -s -XPOST $B/sessions/$SID/generate-lesson | python -c 'import sys,json;d=json.load(sys.stdin);print("reused",d["reused"],len(d["activities"]))'
curl -s -XPOST $B/assessments -H 'content-type: application/json' \
  -d '{"activity_id":1,"student_id":1,"score":1.5,"time_taken_seconds":10}'   # expect 422
```

## 4. Try to break it (adversarial probes)
- Fire two `generate-lesson` requests at the same new session concurrently; expect 3 activities, no 500.
- Boundary scores 0, 0.65, 0.85, 1.0 and just outside; huge numbers; strings for numbers; null; extra fields.
- Unicode/emoji/very long (>200 chars) names and topics; whitespace-only strings; SQL-looking strings.
- `?regenerate=true` on session 1 (has assessments): expect 409 and activities untouched.
- Set `ACCESS_CODE=abc`: check missing/wrong/right header, header case, empty header; `/api/health` stays open.
- Send >limit AI requests quickly; vary `X-Forwarded-For` to see per-IP behaviour.
- CORS: preflight `OPTIONS` with `Origin` and `Access-Control-Request-Headers: x-access-code`; origin not in
  `CORS_ORIGINS` should get no allow-origin header.
- Run `alembic upgrade head`, `downgrade 0001_initial`, `upgrade head` again; run seed twice (second is a no-op).
- Postgres: set `DATABASE_URL=postgresql://user:pass@host/db` (auto-normalised to psycopg2) and repeat
  migration + seed + the manual script. This has only been verified on one Postgres 16 instance.
- If you have an Anthropic key: set `LLM_API_KEY`, confirm `generated_by: "ai"`, section minutes still sum to
  the duration, all 3 levels present. Then set a bad key and confirm a clean fallback with `ai_error`.

## 5. Known limitations (do not report as bugs)
- Level classification averages scores across activities of different difficulty, so an easy-activity 0.9 reads
  as "advanced". Known design flaw, to be revisited with real data.
- Access control is one shared code, not user auth. The rate limiter is in-memory per process.
- No retrieval/RAG yet; the prompt uses only subject, topic, duration and language.
- No endpoints yet for attendance, assessment_items or lesson_feedback (tables exist for onsite data import).
- Repeat assessments for the same student+activity are allowed and each counts toward the average.

## 6. Report format
List findings as: **severity (high/med/low)** · endpoint or file · exact request/steps · expected vs actual ·
suggested fix. Separate "confirmed bugs" from "suspicious but unverified". End with what you did not test.


folder to store all the important documents related to to the project for colllege submission
Overview
Phase	Days	Outcome
1. Foundation + live skeleton	1–2	Clean baseline, new schema, and the current app deployed
2. Core UI workflow	3–5	Multi-view app: select class, plan session, view lesson, enter assessments
3. AI, retrieval, data tooling	6–7	Structured lessons grounded in the corpus, plus CSV import for onsite data
4. Progress and polish	8	Real metrics, loading and error states
5. Harden and ship	9–10	Final tests, honest README, buffer
Phase 1: Foundation and live skeleton (Days 1–2)

Day 1: clean baseline

Create .env.example and update the Anthropic SDK pin and model string.
Reconcile the level thresholds with the seed labels, with one source of truth, and update the fallback counts in the UI.
Replace the seed name "Utkarsh Sharma" with a neutral demo volunteer.
Add Pydantic constraints (score 0–1, positive durations), and check that the student and activity exist before writing an assessment.
Fix duplicate activities on repeated Generate.
Drop torch, sentence-transformers and FAISS from requirements.txt.
Split into Dockerfile.dev and Dockerfile.prod (no --reload, and next build plus next start).
Switch to a system font stack or local fonts.
Write Pytest cases for each fix above, and add a GitHub Actions workflow (lint plus tests).
Produce the CSV templates for onsite collection so you can start preparing.

Day 2: schema and skeleton

Add an Alembic migration with the new tables and columns:
attendance, assessment_items, lesson_feedback
student_code, home_language, volunteer_notes
Define the structured lesson-plan schema (sections, timings, activities per level, materials). The template fallback returns the same shape.
Add endpoints to list classes and sessions, create a class, and create a student.
Add the access-code check and rate limiting.
Deploy to Neon, Render (with migrate on start) and Vercel. I write render.yaml and a click-by-click guide; you do the clicks.

Acceptance (you check): the tests are green in CI, the live URL loads the dashboard with real API data, and a repeated Generate creates no duplicates.

Phase 2: Core UI workflow (Days 3–5)
Day 3: routing and navigation (My Classes, Planner, Progress) with a class selector replacing the hardcoded ID.
Day 4: session configuration form (subject, topic, duration, language, context) and a structured lesson-plan view with loading and error states.
Day 5: assessment entry UI (per student, per question) wired to the backend, with the dashboard updating after saves, plus the volunteer feedback form.

Acceptance: from the live URL, select a class, create a session, generate a lesson, enter assessments for several students, and see the class levels change.

Phase 3: AI, retrieval and data tooling (Days 6–7)
Day 6: write the fractions corpus, build the retriever, and upgrade the prompt (timing, student mix, language, retrieved context). The response includes sources, and the UI shows "grounded in: …". The generated_by badge works both with and without a key.
Day 7: build the CSV import script for the onsite data (validation, clear error messages, safe to re-run), and test it with a fake onsite dataset.

Acceptance: with a key set, the lesson cites sources and respects the duration. Without a key, the template still returns the full schema. The CSV import loads into a clean database.

Phase 4: Progress and polish (Day 8)
Seed 6–8 sessions across weeks for the demo.
Replace the "78%" and "12 sessions" tiles with real queries, add a per-student progress view, and add a score trend.
Finish the frontend form validation, error boundaries and empty states.

Acceptance: every number on the dashboard comes from the database, and a fresh class shows sensible empty states.

Phase 5: Harden and ship (Days 9–10)
Day 9:
Fill in the critical-path test coverage.
Add cost and abuse checks on the AI endpoints (token cap, rate limit).
Deploy checks for CORS, env vars and migrations.
Rewrite the README so it matches the code exactly, including the auth limits.
Write the demo script.
Day 10: buffer. Fix whatever slipped, rehearse the demo, and warm up the free Render instance before presenting.

Acceptance: a full demo run on the live URL with no manual fixes, and every README claim traceable to code.

Risks
Risk	Mitigation
Phase 2 slips (it's the biggest)	It has 3 days, and cut order is feedback form first, then progress polish
Free Render cold start during the demo	Ping it before presenting, or use a paid tier for the demo day
Corpus quality	You or the NGO skim it for accuracy on Day 6
Onsite data arrives mid-plan with unexpected fields	Importer is flexible about optional columns, and the schema changes stay in migrations

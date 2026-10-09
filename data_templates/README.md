# Onsite data collection templates

One CSV per table. Fill them in Google Sheets (works offline on a phone, one tab per file),
then export each tab as CSV. The import script (planned, Phase 3) loads them into the database.

## Rules
- **Pseudonymise.** Use `student_code` (S01, S02, ...) and a first-name `alias` only. No surnames,
  photos, addresses or phone numbers. Keep the real name-to-code list on paper or in a private file
  that is never committed or uploaded.
- Get the NGO's written okay on what you collect.
- Dates are `YYYY-MM-DD`. Yes/no fields are `Y` or `N`.
- Codes are how files link to each other, so keep them stable and unique:
  `class_code` (e.g. G5A), `student_code` (unique within a class), `session_code` (e.g. G5A-001).

## Files and allowed values
| File | Columns |
|---|---|
| `volunteers.csv` | `name`, `email` |
| `classes.csv` | `class_code`, `name`, `grade`, `location`, `volunteer_email` |
| `students.csv` | `student_code`, `alias`, `class_code`, `age`, `home_language`, `teacher_level` (`struggling` / `on_track` / `advanced`), `notes` |
| `sessions.csv` | `session_code`, `class_code`, `date`, `subject`, `topic`, `duration_minutes`, `language`, `planned_by` (`saarthi` / `manual`), `volunteer_notes` |
| `attendance.csv` | `session_code`, `student_code`, `present` (Y/N) |
| `assessment_items.csv` | `session_code`, `student_code`, `question_text`, `difficulty` (`easy` / `medium` / `hard`), `correct` (Y/N), `time_seconds`, `attempts`, `hint_used` (Y/N), `misconception_tag` (optional, e.g. "added denominators") |
| `lesson_feedback.csv` | `session_code`, `rating` (1-5), `what_worked`, `what_didnt`, `time_overran` (Y/N) |

## What to collect first
1. **Baseline diagnostic:** the same 6-8 fractions questions for every student in the first
   session. Record one row per student per question in `assessment_items.csv`, not just a total.
2. **Teacher's level for each child, written down before the diagnostic** (`teacher_level`). Comparing
   it with the computed level is how we check the classification thresholds.
3. **Two or three real sessions with the same group**, so progress over time is real.
4. **The mistakes you actually see** (`misconception_tag`). These feed the lesson content.

## Example rows
`students.csv`: `S01,Aarav,G5A,10,hi,struggling,shy but tries`
`assessment_items.csv`: `G5A-001,S01,"1/4 + 2/4 = ?",easy,Y,35,1,N,`

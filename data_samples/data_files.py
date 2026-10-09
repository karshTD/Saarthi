#!/usr/bin/env python3
"""Generate and validate a synthetic classroom dataset (7 CSV files)."""

import csv
import os
import random
import sys
from datetime import date, timedelta

random.seed(42)

OUT_DIR = "./ngo_data"
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
VOLUNTEER_NAME = "Demo Volunteer"
VOLUNTEER_EMAIL = "demo@saarthi.dev"
CLASS_CODE = "G5A"
CLASS_NAME = "Grade 5 - Section A"
CLASS_GRADE = 5
CLASS_LOCATION = "Demo Centre"

STUDENT_CODES = [f"S{i:02d}" for i in range(1, 11)]
ALIASES = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun",
    "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan",
]
AGES = [9, 10, 11]
HOME_LANGS = ["hi", "mr", "en"]
TEACHER_LEVELS = ["struggling"] * 3 + ["on_track"] * 4 + ["advanced"] * 3
NOTES = [
    "shy but tries",
    "needs encouragement",
    "confident with numbers",
    "sometimes distracted",
    "asks good questions",
    "quiet worker",
    "helps peers",
    "needs extra time",
    "improving steadily",
    "eager to learn",
]

SESSION_CODES = [f"G5A-{i:03d}" for i in range(1, 6)]
TOPICS = [
    "Fractions baseline diagnostic",
    "Like fractions",
    "Adding like fractions",
    "Unlike fractions",
    "Equivalent fractions",
]
SUBJECT = "Mathematics"
DURATION = 45
LANGUAGE = "en"
PLANNED_BY = ["manual", "saarthi", "saarthi", "saarthi", "saarthi"]

# Question bank: 6 questions per session
QUESTION_BANK = {
    1: [  # Fractions baseline diagnostic
        ("1/2 + 1/2 = ?", "easy"),
        ("2/5 + 1/5 = ?", "easy"),
        ("3/8 + 2/8 = ?", "medium"),
        ("1/3 + 1/3 = ?", "medium"),
        ("5/6 - 2/6 = ?", "hard"),
        ("7/10 - 3/10 = ?", "hard"),
    ],
    2: [  # Like fractions
        ("1/4 + 2/4 = ?", "easy"),
        ("3/7 + 2/7 = ?", "easy"),
        ("5/9 + 2/9 = ?", "medium"),
        ("4/11 + 5/11 = ?", "medium"),
        ("7/12 - 3/12 = ?", "hard"),
        ("9/15 - 4/15 = ?", "hard"),
    ],
    3: [  # Adding like fractions
        ("2/6 + 3/6 = ?", "easy"),
        ("4/8 + 1/8 = ?", "easy"),
        ("5/10 + 3/10 = ?", "medium"),
        ("6/13 + 4/13 = ?", "medium"),
        ("8/14 - 2/14 = ?", "hard"),
        ("11/16 - 5/16 = ?", "hard"),
    ],
    4: [  # Unlike fractions
        ("1/2 + 1/4 = ?", "easy"),
        ("1/3 + 1/6 = ?", "easy"),
        ("2/5 + 1/2 = ?", "medium"),
        ("3/4 + 1/8 = ?", "medium"),
        ("5/6 - 1/3 = ?", "hard"),
        ("7/8 - 1/2 = ?", "hard"),
    ],
    5: [  # Equivalent fractions
        ("1/2 = ?/4", "easy"),
        ("2/3 = ?/6", "easy"),
        ("3/4 = ?/8", "medium"),
        ("2/5 = ?/10", "medium"),
        ("5/6 = ?/12", "hard"),
        ("4/7 = ?/14", "hard"),
    ],
}

MISCONCEPTIONS = [
    "added denominators",
    "ignored common denominator",
    "forgot to simplify",
    "compared numerators only",
]

FEEDBACK_TEXTS = [
    ("Students engaged with fraction strips", "Ran out of time for practice", "Y"),
    ("Visual aids helped understanding", "Some students confused with unlike fractions", "N"),
    ("Peer work was effective", "Need more individual attention", "Y"),
    ("Real-life examples worked well", "Too many questions in one session", "N"),
    ("Students showed improvement", "Advanced students were bored", "Y"),
]
FEEDBACK_RATINGS = [4, 3, 5, 2, 4]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def write_csv(filename, header, rows):
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)
        writer.writerows(rows)


def last_week_dates(n):
    """Return n dates, one per week, ending last week (most recent first)."""
    today = date.today()
    # Find last Monday
    last_monday = today - timedelta(days=today.weekday() + 7)
    dates = []
    for i in range(n):
        dates.append(last_monday - timedelta(weeks=n - 1 - i))
    return dates


def ability_for_level(level):
    if level == "struggling":
        return 0.40
    if level == "on_track":
        return 0.70
    return 0.92


def adjust_for_difficulty(base, difficulty):
    if difficulty == "easy":
        return min(base + 0.15, 0.98)
    if difficulty == "medium":
        return base
    return max(base - 0.15, 0.05)


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


# ---------------------------------------------------------------------------
# 1. volunteers.csv
# ---------------------------------------------------------------------------
write_csv("volunteers.csv", ["name", "email"], [[VOLUNTEER_NAME, VOLUNTEER_EMAIL]])

# ---------------------------------------------------------------------------
# 2. classes.csv
# ---------------------------------------------------------------------------
write_csv(
    "classes.csv",
    ["class_code", "name", "grade", "location", "volunteer_email"],
    [[CLASS_CODE, CLASS_NAME, CLASS_GRADE, CLASS_LOCATION, VOLUNTEER_EMAIL]],
)

# ---------------------------------------------------------------------------
# 3. students.csv
# ---------------------------------------------------------------------------
student_rows = []
for i, code in enumerate(STUDENT_CODES):
    alias = ALIASES[i % len(ALIASES)]
    age = AGES[i % len(AGES)]
    lang = HOME_LANGS[i % len(HOME_LANGS)]
    level = TEACHER_LEVELS[i]
    note = f"SYNTHETIC; {NOTES[i]}"
    student_rows.append([code, alias, CLASS_CODE, age, lang, level, note])

write_csv(
    "students.csv",
    ["student_code", "alias", "class_code", "age", "home_language", "teacher_level", "notes"],
    student_rows,
)

# ---------------------------------------------------------------------------
# 4. sessions.csv
# ---------------------------------------------------------------------------
session_dates = last_week_dates(5)
session_rows = []
for i, sc in enumerate(SESSION_CODES):
    d = session_dates[i].isoformat()
    topic = TOPICS[i]
    planned = PLANNED_BY[i]
    vnotes = f"SYNTHETIC; session on {topic.lower()}"
    session_rows.append([sc, CLASS_CODE, d, SUBJECT, topic, DURATION, LANGUAGE, planned, vnotes])

write_csv(
    "sessions.csv",
    ["session_code", "class_code", "date", "subject", "topic",
     "duration_minutes", "language", "planned_by", "volunteer_notes"],
    session_rows,
)

# ---------------------------------------------------------------------------
# 5. attendance.csv
# ---------------------------------------------------------------------------
# Build hidden abilities per student
student_ability = {}
for i, code in enumerate(STUDENT_CODES):
    student_ability[code] = ability_for_level(TEACHER_LEVELS[i])

# Track present students per session
present_map = {}  # session_code -> list of student_codes
attendance_rows = []

for si, sc in enumerate(SESSION_CODES):
    # ~85-95% present => 9 or 10 out of 10
    n_present = random.choice([9, 10])
    present = random.sample(STUDENT_CODES, n_present)
    present_map[sc] = present
    for code in STUDENT_CODES:
        is_present = "Y" if code in present else "N"
        attendance_rows.append([sc, code, is_present])

write_csv("attendance.csv", ["session_code", "student_code", "present"], attendance_rows)

# ---------------------------------------------------------------------------
# 6. assessment_items.csv
# ---------------------------------------------------------------------------
assessment_rows = []
for si, sc in enumerate(SESSION_CODES):
    session_idx = si  # 0-based
    improvement = 0.04 * session_idx
    questions = QUESTION_BANK[si + 1]
    for code in present_map[sc]:
        base = student_ability[code]
        effective = clamp(base + improvement, 0.05, 0.98)
        for q_text, difficulty in questions:
            p_correct = adjust_for_difficulty(effective, difficulty)
            correct = "Y" if random.random() < p_correct else "N"

            # time_seconds 15-240 (longer for wrong/hard)
            if correct == "Y":
                if difficulty == "easy":
                    t = random.randint(15, 60)
                elif difficulty == "medium":
                    t = random.randint(30, 120)
                else:
                    t = random.randint(60, 180)
            else:
                if difficulty == "easy":
                    t = random.randint(30, 120)
                elif difficulty == "medium":
                    t = random.randint(60, 180)
                else:
                    t = random.randint(90, 240)

            # attempts 1-3 (more for wrong)
            if correct == "Y":
                attempts = random.choice([1, 1, 1, 2])
            else:
                attempts = random.choice([1, 2, 2, 3])

            # hint_used Y mostly for struggling students on hard questions
            level = TEACHER_LEVELS[STUDENT_CODES.index(code)]
            if level == "struggling" and difficulty == "hard":
                hint = "Y" if random.random() < 0.7 else "N"
            elif level == "struggling" and difficulty == "medium":
                hint = "Y" if random.random() < 0.4 else "N"
            elif level == "on_track" and difficulty == "hard":
                hint = "Y" if random.random() < 0.3 else "N"
            else:
                hint = "Y" if random.random() < 0.1 else "N"

            # misconception_tag only on wrong answers
            if correct == "N":
                misconception = random.choice(MISCONCEPTIONS)
            else:
                misconception = ""

            assessment_rows.append([
                sc, code, q_text, difficulty, correct,
                t, attempts, hint, misconception
            ])

write_csv(
    "assessment_items.csv",
    ["session_code", "student_code", "question_text", "difficulty",
     "correct", "time_seconds", "attempts", "hint_used", "misconception_tag"],
    assessment_rows,
)

# ---------------------------------------------------------------------------
# 7. lesson_feedback.csv
# ---------------------------------------------------------------------------
feedback_rows = []
for i, sc in enumerate(SESSION_CODES):
    worked, didnt, overran = FEEDBACK_TEXTS[i]
    rating = FEEDBACK_RATINGS[i]
    feedback_rows.append([sc, rating, worked, didnt, overran])

write_csv(
    "lesson_feedback.csv",
    ["session_code", "rating", "what_worked", "what_didnt", "time_overran"],
    feedback_rows,
)

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
errors = []


def read_csv(filename):
    path = os.path.join(OUT_DIR, filename)
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


try:
    volunteers = read_csv("volunteers.csv")
    classes = read_csv("classes.csv")
    students = read_csv("students.csv")
    sessions = read_csv("sessions.csv")
    attendance = read_csv("attendance.csv")
    assessments = read_csv("assessment_items.csv")
    feedback = read_csv("lesson_feedback.csv")
except Exception as e:
    print(f"FATAL: could not read CSV files: {e}", file=sys.stderr)
    sys.exit(1)

# Build lookup sets
volunteer_emails = {v["email"] for v in volunteers}
class_codes = {c["class_code"] for c in classes}
student_codes_set = {s["student_code"] for s in students}
session_codes_set = {s["session_code"] for s in sessions}
class_student_map = {}
for s in students:
    class_student_map.setdefault(s["class_code"], set()).add(s["student_code"])

# Check every class_code used exists
for s in sessions:
    if s["class_code"] not in class_codes:
        errors.append(f"Session {s['session_code']} references unknown class {s['class_code']}")
for s in students:
    if s["class_code"] not in class_codes:
        errors.append(f"Student {s['student_code']} references unknown class {s['class_code']}")

# Check volunteer_email in classes exists
for c in classes:
    if c["volunteer_email"] not in volunteer_emails:
        errors.append(f"Class {c['class_code']} references unknown volunteer {c['volunteer_email']}")

# Check session_code references in attendance, assessments, feedback
for a in attendance:
    if a["session_code"] not in session_codes_set:
        errors.append(f"Attendance references unknown session {a['session_code']}")
    if a["student_code"] not in student_codes_set:
        errors.append(f"Attendance references unknown student {a['student_code']}")
for a in assessments:
    if a["session_code"] not in session_codes_set:
        errors.append(f"Assessment references unknown session {a['session_code']}")
    if a["student_code"] not in student_codes_set:
        errors.append(f"Assessment references unknown student {a['student_code']}")
for f in feedback:
    if f["session_code"] not in session_codes_set:
        errors.append(f"Feedback references unknown session {f['session_code']}")

# No duplicate (session_code, student_code, question_text)
seen = set()
for a in assessments:
    key = (a["session_code"], a["student_code"], a["question_text"])
    if key in seen:
        errors.append(f"Duplicate assessment row: {key}")
    seen.add(key)

# Absent students have no assessment rows
present_set = set()
for a in attendance:
    if a["present"] == "Y":
        present_set.add((a["session_code"], a["student_code"]))
for a in assessments:
    key = (a["session_code"], a["student_code"])
    if key not in present_set:
        errors.append(f"Assessment row for absent student: {key}")

# SYNTHETIC flag in notes / volunteer_notes
for s in students:
    if not s["notes"].startswith("SYNTHETIC"):
        errors.append(f"Student {s['student_code']} notes missing SYNTHETIC")
for s in sessions:
    if not s["volunteer_notes"].startswith("SYNTHETIC"):
        errors.append(f"Session {s['session_code']} volunteer_notes missing SYNTHETIC")

if errors:
    print("VALIDATION FAILED:", file=sys.stderr)
    for e in errors:
        print(f"  - {e}", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("=" * 60)
print("SYNTHETIC CLASSROOM DATASET - VALIDATION SUMMARY")
print("=" * 60)
print(f"volunteers.csv:        {len(volunteers)} rows")
print(f"classes.csv:           {len(classes)} rows")
print(f"students.csv:          {len(students)} rows")
print(f"sessions.csv:          {len(sessions)} rows")
print(f"attendance.csv:        {len(attendance)} rows")
print(f"assessment_items.csv:  {len(assessments)} rows")
print(f"lesson_feedback.csv:   {len(feedback)} rows")
print()

# Per-student accuracy in session 001 vs 005
def accuracy(session_code):
    acc = {}
    for a in assessments:
        if a["session_code"] != session_code:
            continue
        code = a["student_code"]
        if code not in acc:
            acc[code] = [0, 0]
        acc[code][1] += 1
        if a["correct"] == "Y":
            acc[code][0] += 1
    return {k: (v[0] / v[1] if v[1] else 0.0) for k, v in acc.items()}


acc1 = accuracy("G5A-001")
acc5 = accuracy("G5A-005")

print("Per-student accuracy: Session 001 vs Session 005")
print("-" * 50)
print(f"{'Student':<10} {'S001':>8} {'S005':>8} {'Change':>8}")
print("-" * 50)
improved = 0
compared = 0
for code in STUDENT_CODES:
    if code in acc1 and code in acc5:
        a1 = acc1[code]
        a5 = acc5[code]
        diff = a5 - a1
        compared += 1
        if diff > 0:
            improved += 1
        marker = " ↑" if diff > 0 else (" ↓" if diff < 0 else " →")
        print(f"{code:<10} {a1:>8.1%} {a5:>8.1%} {diff:>+7.1%}{marker}")
print("-" * 50)
print(f"Students improved: {improved}/{compared}")
print()
print("All validations passed.")

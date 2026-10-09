"""
Generates a structured, timed lesson plan with one activity per ability level.

Two modes, chosen automatically and always labelled in the response:
  - "ai":       settings.llm_api_key is set -> Claude generates the plan as JSON, which is
                validated against LessonPlan. Any failure (network, bad JSON, wrong shape)
                falls back to the template and reports ai_error.
  - "template": no key, or AI failed -> deterministic, topic-aware plan.
"""
import logging

from app.ai.llm import complete, extract_json, safe_error
from app.core.config import settings
from app.schemas.lesson import LEVELS, LessonActivity, LessonPlan, LessonSection

logger = logging.getLogger(__name__)

# (name, share of the session, description)
_TEMPLATE_SECTIONS = [
    ("Warm-up and recap", 0.10, "Quick questions to recall what the class already knows."),
    ("Introduce the idea", 0.25, "Show the concept with a concrete example on the board."),
    ("Guided practice", 0.25, "Work through examples together, asking students to explain steps."),
    ("Differentiated activities", 0.25, "Students work on the activity matched to their level."),
    ("Check understanding", 0.10, "Short assessment; record each student's responses."),
    ("Wrap-up", 0.05, "Recap the key idea and preview the next session."),
]

_TEMPLATE_ACTIVITIES = {
    "struggling": (
        "Visual, step-by-step walkthrough",
        "Using {topic}, draw it step by step with a worked example, then let the student "
        "repeat it with a similar example.",
    ),
    "on_track": (
        "Grade-level practice",
        "Give three practice problems on {topic} at grade level and ask students to explain "
        "their method.",
    ),
    "advanced": (
        "Extension challenge",
        "Pose a problem that applies {topic} in a new context, such as sharing or measuring, "
        "and ask for more than one way to solve it.",
    ),
}


def fit_minutes(weights: list[float], total: int) -> list[int]:
    """Split `total` minutes proportionally to `weights`: integers >= 1 summing exactly to total."""
    n = len(weights)
    if n == 0 or total < n:
        raise ValueError("cannot fit sections into the session duration")
    scale = sum(weights)
    raw = [w / scale * total for w in weights]
    out = [max(1, int(r)) for r in raw]
    diff = total - sum(out)
    order = sorted(range(n), key=lambda i: raw[i] - int(raw[i]), reverse=diff > 0)
    i = 0
    while diff != 0:
        idx = order[i % n]
        if diff > 0:
            out[idx] += 1
            diff -= 1
        elif out[idx] > 1:
            out[idx] -= 1
            diff += 1
        i += 1
    return out


def _template_plan(subject: str, topic: str, duration: int) -> LessonPlan:
    minutes = fit_minutes([share for _, share, _ in _TEMPLATE_SECTIONS], duration)
    sections = [
        LessonSection(name=name, minutes=m, description=desc)
        for (name, _, desc), m in zip(_TEMPLATE_SECTIONS, minutes, strict=True)
    ]
    activities = [
        LessonActivity(
            level=level,
            title=f"{topic}: {_TEMPLATE_ACTIVITIES[level][0]}",
            prompt=_TEMPLATE_ACTIVITIES[level][1].format(topic=topic.lower()),
            materials=["Whiteboard or paper", "Pencils"],
        )
        for level in LEVELS
    ]
    return LessonPlan(
        title=f"{subject}: {topic}",
        objective=f"Students understand {topic.lower()} and practise it at their own level.",
        total_minutes=duration,
        sections=sections,
        activities=activities,
        materials=["Whiteboard or paper", "Pencils"],
    )


_SYSTEM = (
    "You write short, practical lesson plans for NGO volunteer tutors teaching children of "
    "mixed ability. Respond with ONLY a JSON object, no markdown, shaped exactly like:\n"
    '{"title": str, "objective": str, "sections": [{"name": str, "minutes": int, '
    '"description": str}], "activities": [{"level": "struggling"|"on_track"|"advanced", '
    '"title": str, "prompt": str, "answer": str, "materials": [str]}], "materials": [str]}\n'
    "Rules: 4-6 sections whose minutes add up to the session duration; exactly three "
    "activities, one per level; every prompt is one or two sentences, concrete, and usable "
    "with no extra materials beyond paper and a board."
)


def _ai_plan(subject: str, topic: str, duration: int, language: str) -> LessonPlan:
    user = (
        f"Subject: {subject}\nTopic: {topic}\nSession duration: {duration} minutes\n"
        f"Write all student-facing text in the language with code '{language}'."
    )
    data = extract_json(complete(_SYSTEM, user, max_tokens=1800))
    sections = data.get("sections") or []
    minutes = fit_minutes([max(1, int(s.get("minutes", 1))) for s in sections], duration)
    for section, m in zip(sections, minutes, strict=True):
        section["minutes"] = m
    data["total_minutes"] = duration
    data["sources"] = []
    return LessonPlan.model_validate(data)


def generate_lesson(
    subject: str, topic: str, duration_minutes: int = 45, language: str = "en"
) -> dict:
    """Returns {"plan": LessonPlan, "generated_by": "ai"|"template", "ai_error": str|None}."""
    if settings.llm_api_key:
        try:
            plan = _ai_plan(subject, topic, duration_minutes, language)
            return {"plan": plan, "generated_by": "ai", "ai_error": None}
        except Exception as exc:  # noqa: BLE001 - degrade to the template, never 500
            logger.warning("AI lesson generation failed: %s", exc)
            return {
                "plan": _template_plan(subject, topic, duration_minutes),
                "generated_by": "template",
                "ai_error": safe_error(exc),
            }
    return {
        "plan": _template_plan(subject, topic, duration_minutes),
        "generated_by": "template",
        "ai_error": None,
    }

"""
Generates differentiated activities for a topic across three levels
(struggling / on_track / advanced).

Two modes, chosen automatically:
  - "ai": settings.llm_api_key is set -> calls Claude for real, structured
    generation grounded in the topic and subject.
  - "template": no key configured -> deterministic, topic-aware templates.
    Not a placeholder for demo purposes only — it's a legitimate offline
    fallback so the product still works if the LLM call fails or no key
    is configured, and the response is honestly labeled either way.
"""
import json
import re

from app.core.config import settings

LEVELS = ["struggling", "on_track", "advanced"]

LEVEL_FRAMING = {
    "struggling": "a visual, step-by-step introduction with a worked example",
    "on_track": "a direct practice problem at grade level",
    "advanced": "an extension problem that applies the concept in a new context",
}


def _template_activity(subject: str, topic: str, level: str) -> dict:
    framing = LEVEL_FRAMING[level]
    return {
        "level": level,
        "title": f"{topic}: {framing.split(',')[0]}",
        "prompt": f"({subject}) Using {topic.lower()}, give students {framing}.",
        "generated_by": "template",
    }


def _generate_template(subject: str, topic: str) -> dict:
    return {
        "subject": subject,
        "topic": topic,
        "activities": [_template_activity(subject, topic, lvl) for lvl in LEVELS],
        "generated_by": "template",
    }


def _generate_ai(subject: str, topic: str) -> dict:
    import anthropic

    client = anthropic.Anthropic(api_key=settings.llm_api_key)

    system = (
        "You write short, differentiated classroom activities for NGO volunteer "
        "tutors teaching children with mixed ability levels. Respond with ONLY "
        "valid JSON, no markdown fences, matching this shape: "
        '{"activities": [{"level": "struggling", "title": "...", "prompt": "..."}, '
        '{"level": "on_track", ...}, {"level": "advanced", ...}]}. '
        "Each prompt should be one to two sentences, concrete, and immediately "
        "usable by a volunteer with no extra materials."
    )
    user = f"Subject: {subject}\nTopic: {topic}\nGenerate the three differentiated activities."

    response = client.messages.create(
        model=settings.llm_model,
        max_tokens=600,
        system=system,
        messages=[{"role": "user", "content": user}],
    )

    text = "".join(block.text for block in response.content if block.type == "text")
    text = re.sub(r"^```(json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    parsed = json.loads(text)

    activities = parsed["activities"]
    for a in activities:
        a["generated_by"] = "ai"

    return {"subject": subject, "topic": topic, "activities": activities, "generated_by": "ai"}


def generate_lesson(subject: str, topic: str) -> dict:
    if not settings.llm_api_key:
        return _generate_template(subject, topic)

    try:
        return _generate_ai(subject, topic)
    except Exception as exc:  # noqa: BLE001 - demo must degrade gracefully, not 500
        fallback = _generate_template(subject, topic)
        fallback["ai_error"] = str(exc)
        return fallback

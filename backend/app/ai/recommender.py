"""
Turns a class analysis into a plain-language next-session recommendation.
Same dual-mode pattern as lesson_generator: Claude when a key is configured,
an honest rule-based summary otherwise.
"""
import json
import logging

from app.ai.llm import complete, extract_json, safe_error
from app.core.config import settings

logger = logging.getLogger(__name__)

_SYSTEM = (
    "You write short, plain-language recommendations for an NGO volunteer tutor about what to "
    'teach next session, based on a class performance summary. Respond with ONLY JSON: '
    '{"recommendation": "..."}. Two to three sentences, concrete, no jargon.'
)


def _template_recommendation(analysis: dict, topic: str) -> dict:
    counts = analysis["level_counts"]
    parts = []
    if counts.get("advanced"):
        parts.append(f"{counts['advanced']} student(s) are ready to move beyond {topic}.")
    if counts.get("on_track"):
        parts.append(
            f"{counts['on_track']} student(s) are on track and can continue at the current pace."
        )
    if counts.get("struggling"):
        parts.append(
            f"{counts['struggling']} student(s) need another pass on the core concept "
            "before advancing."
        )
    text = " ".join(parts) if parts else "Not enough assessment data yet to make a recommendation."
    return {"recommendation": text, "generated_by": "template"}


def _ai_recommendation(analysis: dict, topic: str) -> dict:
    user = f"Topic just taught: {topic}\nClass performance summary: {json.dumps(analysis)}"
    parsed = extract_json(complete(_SYSTEM, user, max_tokens=300))
    text = parsed.get("recommendation")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("missing recommendation text")
    return {"recommendation": text.strip(), "generated_by": "ai"}


def generate_recommendation(analysis: dict, topic: str) -> dict:
    if not settings.llm_api_key:
        return _template_recommendation(analysis, topic)
    try:
        return _ai_recommendation(analysis, topic)
    except Exception as exc:  # noqa: BLE001
        logger.warning("AI recommendation failed: %s", exc)
        fallback = _template_recommendation(analysis, topic)
        fallback["ai_error"] = safe_error(exc)
        return fallback

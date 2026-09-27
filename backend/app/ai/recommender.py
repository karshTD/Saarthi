"""
Turns a class analysis result into a plain-language next-session
recommendation. Same dual-mode pattern as lesson_generator: real Claude
call when a key is configured, an honest rule-based summary otherwise.
"""
from app.core.config import settings


def _template_recommendation(analysis: dict, topic: str) -> dict:
    counts = analysis["level_counts"]
    parts = []
    if counts.get("advanced"):
        parts.append(f"{counts['advanced']} student(s) are ready to move beyond {topic}.")
    if counts.get("on_track"):
        parts.append(f"{counts['on_track']} student(s) are on track and can continue at the current pace.")
    if counts.get("struggling"):
        parts.append(f"{counts['struggling']} student(s) need another pass on the core concept before advancing.")

    text = " ".join(parts) if parts else "Not enough assessment data yet to make a recommendation."
    return {"recommendation": text, "generated_by": "template"}


def _ai_recommendation(analysis: dict, topic: str) -> dict:
    import anthropic
    import json
    import re

    client = anthropic.Anthropic(api_key=settings.llm_api_key)

    system = (
        "You write short, plain-language recommendations for an NGO volunteer "
        "tutor about what to teach next session, based on a class performance "
        "summary. Respond with ONLY valid JSON: {\"recommendation\": \"...\"}. "
        "Two to three sentences, concrete, no jargon."
    )
    user = f"Topic just taught: {topic}\nClass performance summary: {json.dumps(analysis)}"

    response = client.messages.create(
        model=settings.llm_model,
        max_tokens=300,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    text = "".join(block.text for block in response.content if block.type == "text")
    text = re.sub(r"^```(json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    parsed = json.loads(text)
    parsed["generated_by"] = "ai"
    return parsed


def generate_recommendation(analysis: dict, topic: str) -> dict:
    if not settings.llm_api_key:
        return _template_recommendation(analysis, topic)

    try:
        return _ai_recommendation(analysis, topic)
    except Exception as exc:  # noqa: BLE001
        fallback = _template_recommendation(analysis, topic)
        fallback["ai_error"] = str(exc)
        return fallback

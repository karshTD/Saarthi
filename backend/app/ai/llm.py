"""Thin wrapper around the Anthropic SDK so every AI feature shares one call path."""
import json

from app.core.config import settings


def complete(system: str, user: str, max_tokens: int) -> str:
    import anthropic

    client = anthropic.Anthropic(api_key=settings.llm_api_key, timeout=45.0, max_retries=1)
    response = client.messages.create(
        model=settings.llm_model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return "".join(block.text for block in response.content if block.type == "text")


def extract_json(text: str) -> dict:
    """Pull the first JSON object out of model output, tolerating markdown fences."""
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        raise ValueError("no JSON object in model output")
    parsed = json.loads(text[start : end + 1])
    if not isinstance(parsed, dict):
        raise ValueError("model output is not a JSON object")
    return parsed


def safe_error(exc: Exception) -> str:
    """Short, non-leaky description of an AI failure that is safe to return to clients."""
    return type(exc).__name__

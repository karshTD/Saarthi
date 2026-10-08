from unittest.mock import MagicMock, patch

from app.ai.lesson_generator import _generate_ai
from app.core.config import Settings, settings


def test_anthropic_model_env_happy_path(monkeypatch):
    """Happy path: test that ANTHROPIC_MODEL environment variable is used by Settings and AI client."""
    custom_model = "claude-3-5-haiku-20241022"
    monkeypatch.setenv("ANTHROPIC_MODEL", custom_model)

    new_settings = Settings()
    assert new_settings.llm_model == custom_model

    monkeypatch.setattr(settings, "llm_api_key", "test-key")
    monkeypatch.setattr(settings, "llm_model", custom_model)

    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [
        MagicMock(
            type="text",
            text='{"activities": [{"level": "struggling", "title": "t", "prompt": "p"}]}',
        )
    ]
    mock_client.messages.create.return_value = mock_response

    with patch("anthropic.Anthropic", return_value=mock_client):
        _generate_ai("Math", "Fractions")

    mock_client.messages.create.assert_called_once()
    _, kwargs = mock_client.messages.create.call_args
    assert kwargs["model"] == custom_model


def test_anthropic_model_env_fallback_path(monkeypatch):
    """Failure/fallback path: test that when ANTHROPIC_MODEL is unset, default fallback model is used."""
    monkeypatch.delenv("ANTHROPIC_MODEL", raising=False)

    new_settings = Settings()
    assert new_settings.llm_model == "claude-3-5-sonnet-20241022"

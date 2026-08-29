import pytest
from pydantic import SecretStr, ValidationError

from app.config import Settings


def test_defaults_to_unconfigured_google_ai_studio() -> None:
    settings = Settings(_env_file=None)

    assert settings.ai_provider == "google_ai_studio"
    assert settings.ai_configured is False


def test_detects_a_google_ai_studio_key_without_exposing_it() -> None:
    settings = Settings(_env_file=None, google_api_key=SecretStr("fictional-key"))

    assert settings.ai_provider == "google_ai_studio"
    assert settings.ai_configured is True
    assert "fictional-key" not in repr(settings)


def test_vertex_ai_requires_a_cloud_project() -> None:
    settings = Settings(_env_file=None, google_genai_use_vertexai=True)

    assert settings.ai_provider == "vertex_ai"
    assert settings.ai_configured is False

    configured = Settings(
        _env_file=None,
        google_genai_use_vertexai=True,
        google_cloud_project="fictional-project",
    )
    assert configured.ai_configured is True


def test_upload_limit_cannot_be_configured_above_twenty_megabytes() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, max_upload_mb=21)

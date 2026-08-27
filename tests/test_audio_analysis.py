from types import SimpleNamespace

from app.config import Settings
from app.schemas import AnalysisResult, RiskLevel
from app.services import audio_analysis


def test_builds_a_structured_audio_gemini_request(monkeypatch) -> None:
    expected = AnalysisResult(
        risk_level=RiskLevel.BE_CAREFUL,
        summary="The caller asks for information that should be independently verified.",
        warning_signs=[],
        uncertainty=["The caller's identity cannot be confirmed from the recording."],
        safe_next_steps=["Use an independently found official number to verify the request."],
    )
    calls = {}

    class FakeModels:
        def generate_content(self, **kwargs):
            calls.update(kwargs)
            return SimpleNamespace(parsed=expected, text=None)

    fake_client = SimpleNamespace(models=FakeModels())
    monkeypatch.setattr(audio_analysis, "build_gemini_client", lambda settings: fake_client)
    settings = Settings(
        _env_file=None,
        google_genai_use_vertexai=True,
        google_cloud_project="fictional-project",
    )

    result = audio_analysis.analyse_audio(
        audio_bytes=b"RIFF\x00\x00\x00\x00WAVEfictional",
        content_type="audio/x-wav",
        settings=settings,
    )

    assert result == expected
    assert calls["model"] == "gemini-3.5-flash"
    assert len(calls["contents"]) == 2
    assert calls["contents"][1].inline_data.mime_type == "audio/wav"
    assert calls["contents"][1].inline_data.data.endswith(b"fictional")
    assert calls["config"].response_mime_type == "application/json"


def test_rejects_an_empty_audio_request() -> None:
    settings = Settings(_env_file=None)

    try:
        audio_analysis.analyse_audio(
            audio_bytes=b"",
            content_type="audio/mpeg",
            settings=settings,
        )
    except audio_analysis.AudioAnalysisError as exc:
        assert "required" in str(exc)
    else:
        raise AssertionError("An empty audio request should fail before calling Gemini.")

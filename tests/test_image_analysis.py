from types import SimpleNamespace

from app.config import Settings
from app.schemas import AnalysisResult, RiskLevel
from app.services import image_analysis


def test_builds_a_structured_multimodal_gemini_request(monkeypatch) -> None:
    expected = AnalysisResult(
        risk_level=RiskLevel.BE_CAREFUL,
        summary="The request should be independently verified.",
        warning_signs=[],
        uncertainty=["The sender cannot be confirmed from this image."],
        safe_next_steps=["Use an official website to contact the organisation."],
    )
    calls = {}

    class FakeModels:
        def generate_content(self, **kwargs):
            calls.update(kwargs)
            return SimpleNamespace(parsed=expected, text=None)

    fake_client = SimpleNamespace(models=FakeModels())
    monkeypatch.setattr(image_analysis, "build_gemini_client", lambda settings: fake_client)
    settings = Settings(
        _env_file=None,
        google_genai_use_vertexai=True,
        google_cloud_project="fictional-project",
    )

    result = image_analysis.analyse_images(
        image_items=[
            (b"\x89PNG\r\n\x1a\npage one", "image/png"),
            (b"\xff\xd8\xffpage two", "image/jpeg"),
        ],
        settings=settings,
    )

    assert result == expected
    assert calls["model"] == "gemini-3.5-flash"
    assert len(calls["contents"]) == 5
    assert calls["contents"][1] == "Page 1 of 2:"
    assert calls["contents"][3] == "Page 2 of 2:"
    assert "do not combine them into one narrative" in calls["contents"][0]
    assert "use the highest risk found" in calls["contents"][0]
    assert "return 1 to 3 low_concern_reasons" in calls["contents"][0]
    assert "Do not treat" in calls["contents"][0]
    assert calls["config"].response_mime_type == "application/json"

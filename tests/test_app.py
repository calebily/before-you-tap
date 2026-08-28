from fastapi.testclient import TestClient

import app.main as main_module
from app.config import Settings
from app.main import app
from app.schemas import AnalysisResult, RiskLevel, WarningSign

client = TestClient(app)


def test_home_page_loads() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "Before You Tap" in response.text
    assert 'rel="icon" href="/static/logo.svg"' in response.text
    assert 'class="brand-logo" src="/static/logo.svg"' in response.text
    assert "Check before you act." in response.text
    assert "Photo or screenshot" in response.text
    assert "Check an audio message" in response.text
    assert "Listen" in response.text
    assert "Drag image pages here" in response.text
    assert "Take a photo" in response.text
    assert 'id="camera-input"' in response.text
    assert 'capture="environment"' in response.text
    assert "Paste a screenshot" in response.text
    assert "⌘V on Mac" in response.text
    assert "Ctrl+V on Windows" in response.text
    assert 'id="paste-image"' not in response.text
    assert "Check unrelated emails or conversations separately" in response.text
    assert "Add another image" not in response.text
    assert "Drag an audio file here" in response.text
    assert "Remove audio" in response.text
    assert "See the full report" in response.text


def test_logo_asset_loads() -> None:
    response = client.get("/static/logo.svg")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/svg+xml")
    assert "Before You Tap" in response.text


def test_health_check_is_safe_without_cloud_credentials() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "before-you-tap",
        "model": "gemini-3.5-flash",
        "ai_provider": "google_ai_studio",
        "ai_configured": False,
        "cloud_configured": False,
    }


def test_validates_a_real_png_signature_without_storing_the_file() -> None:
    png = b"\x89PNG\r\n\x1a\n" + b"fictional image bytes"

    response = client.post(
        "/api/uploads/validate",
        files={"file": ("fictional-scam.png", png, "image/png")},
    )

    assert response.status_code == 200
    assert response.json() == {
        "filename": "fictional-scam.png",
        "media_kind": "image",
        "content_type": "image/png",
        "size_bytes": len(png),
        "ai_provider": "google_ai_studio",
        "ai_configured": False,
        "message": "The file is valid and ready for analysis.",
    }


def test_rejects_a_file_with_a_misleading_image_type() -> None:
    response = client.post(
        "/api/uploads/validate",
        files={"file": ("not-an-image.png", b"plain text", "image/png")},
    )

    assert response.status_code == 400
    assert "do not match" in response.json()["detail"]


def test_rejects_an_unsupported_upload_type() -> None:
    response = client.post(
        "/api/uploads/validate",
        files={"file": ("document.pdf", b"%PDF-fictional", "application/pdf")},
    )

    assert response.status_code == 400
    assert "supported image or audio" in response.json()["detail"]


def test_analyses_ordered_images_together_without_storing_them(monkeypatch) -> None:
    expected = AnalysisResult(
        risk_level=RiskLevel.HIGH_RISK,
        summary="This message shows several common scam warning signs.",
        warning_signs=[
            WarningSign(
                title="Urgent payment request",
                evidence="The message says payment is required immediately.",
                explanation="Pressure to pay quickly can stop you from checking the request.",
            )
        ],
        uncertainty=["The sender's identity cannot be confirmed from the image alone."],
        safe_next_steps=[
            "Pause. Do not reply, pay, click links, or share information.",
            "Contact the organisation using a number from its official website.",
            "Talk to someone you trust before taking action.",
        ],
    )

    def fake_analyse_images(*, image_items, settings):
        assert len(image_items) == 2
        assert image_items[0][0].endswith(b"page one")
        assert image_items[1][0].endswith(b"page two")
        assert [item[1] for item in image_items] == ["image/png", "image/png"]
        assert settings.gemini_model == "gemini-3.5-flash"
        return expected

    monkeypatch.setattr(main_module, "analyse_images", fake_analyse_images)
    png_header = b"\x89PNG\r\n\x1a\n"

    response = client.post(
        "/api/analyse/images",
        files=[
            ("files", ("page-1.png", png_header + b"page one", "image/png")),
            ("files", ("page-2.png", png_header + b"page two", "image/png")),
        ],
    )

    assert response.status_code == 200
    assert response.json() == expected.model_dump(mode="json")


def test_image_analysis_rejects_audio_before_calling_gemini(monkeypatch) -> None:
    def fail_if_called(**kwargs):
        raise AssertionError("Gemini should not be called for audio on the image endpoint.")

    monkeypatch.setattr(main_module, "analyse_images", fail_if_called)

    response = client.post(
        "/api/analyse/images",
        files={"files": ("fictional-message.mp3", b"ID3fictional", "audio/mpeg")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Please choose supported image files only."


def test_image_analysis_rejects_more_than_five_images(monkeypatch) -> None:
    def fail_if_called(**kwargs):
        raise AssertionError("Gemini should not be called for too many images.")

    monkeypatch.setattr(main_module, "analyse_images", fail_if_called)
    png = b"\x89PNG\r\n\x1a\nfictional"

    response = client.post(
        "/api/analyse/images",
        files=[("files", (f"page-{number}.png", png, "image/png")) for number in range(6)],
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Please choose no more than 5 images."


def test_image_analysis_enforces_the_combined_size_limit(monkeypatch) -> None:
    def fail_if_called(**kwargs):
        raise AssertionError("Gemini should not be called for an oversized group.")

    settings = Settings(_env_file=None, max_upload_mb=1)
    monkeypatch.setattr(main_module, "get_settings", lambda: settings)
    monkeypatch.setattr(main_module, "analyse_images", fail_if_called)
    png_header = b"\x89PNG\r\n\x1a\n"
    large_page = png_header + (b"x" * 600_000)

    response = client.post(
        "/api/analyse/images",
        files=[
            ("files", ("page-1.png", large_page, "image/png")),
            ("files", ("page-2.png", large_page, "image/png")),
        ],
    )

    assert response.status_code == 413
    assert "too large together" in response.json()["detail"]


def test_analyses_saved_audio_without_storing_it(monkeypatch) -> None:
    expected = AnalysisResult(
        risk_level=RiskLevel.HIGH_RISK,
        summary="The caller uses pressure and asks for private banking information.",
        warning_signs=[
            WarningSign(
                title="Request for private information",
                evidence="The caller asks for the listener's banking password.",
                explanation="A legitimate organisation should not ask for a password by phone.",
            )
        ],
        uncertainty=["The caller's identity cannot be confirmed from the audio."],
        safe_next_steps=[
            "Pause. Do not call back, pay, follow instructions, or share information.",
            "Contact the bank using the number on the back of your card.",
            "Talk to someone you trust before taking action.",
        ],
    )

    def fake_analyse_audio(*, audio_bytes, content_type, settings):
        assert audio_bytes.endswith(b"fictional voicemail")
        assert content_type == "audio/wav"
        assert settings.gemini_model == "gemini-3.5-flash"
        return expected

    monkeypatch.setattr(main_module, "analyse_audio", fake_analyse_audio)
    wav = b"RIFF\x00\x00\x00\x00WAVEfictional voicemail"

    response = client.post(
        "/api/analyse/audio",
        files={"file": ("fictional-voicemail.wav", wav, "audio/wav")},
    )

    assert response.status_code == 200
    assert response.json() == expected.model_dump(mode="json")


def test_audio_analysis_rejects_an_image_before_calling_gemini(monkeypatch) -> None:
    def fail_if_called(**kwargs):
        raise AssertionError("Gemini should not be called for an image on the audio endpoint.")

    monkeypatch.setattr(main_module, "analyse_audio", fail_if_called)
    png = b"\x89PNG\r\n\x1a\nfictional"

    response = client.post(
        "/api/analyse/audio",
        files={"file": ("fictional-message.png", png, "image/png")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Please choose a supported audio file only."

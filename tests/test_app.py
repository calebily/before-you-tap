from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home_page_loads() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "Before You Tap" in response.text
    assert "Check an audio message" in response.text


def test_health_check_is_safe_without_cloud_credentials() -> None:
    response = client.get("/healthz")

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
        "message": "The file is ready. AI analysis is not connected yet.",
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

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
        "cloud_configured": False,
    }

import pytest

from app.schemas import MediaKind
from app.services.file_validation import FileValidationError, validate_upload


def test_accepts_supported_image() -> None:
    result = validate_upload(content_type="image/png", size_bytes=100, max_bytes=1_000)

    assert result.media_kind is MediaKind.IMAGE


def test_accepts_supported_audio() -> None:
    result = validate_upload(content_type="audio/mpeg", size_bytes=100, max_bytes=1_000)

    assert result.media_kind is MediaKind.AUDIO


@pytest.mark.parametrize(
    ("content_type", "size_bytes", "message"),
    [
        ("application/pdf", 100, "supported image or audio"),
        ("image/png", 0, "empty"),
        ("image/png", 1_001, "too large"),
    ],
)
def test_rejects_unsafe_uploads(content_type: str, size_bytes: int, message: str) -> None:
    with pytest.raises(FileValidationError, match=message):
        validate_upload(content_type=content_type, size_bytes=size_bytes, max_bytes=1_000)

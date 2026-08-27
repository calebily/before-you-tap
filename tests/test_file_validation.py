import pytest

from app.schemas import MediaKind
from app.services.file_validation import (
    FileValidationError,
    validate_file_content,
    validate_upload,
)


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


@pytest.mark.parametrize(
    ("content_type", "content"),
    [
        ("image/jpeg", b"\xff\xd8\xfffictional"),
        ("image/png", b"\x89PNG\r\n\x1a\nfictional"),
        ("image/webp", b"RIFF\x00\x00\x00\x00WEBPfictional"),
        ("audio/mpeg", b"ID3fictional"),
        ("audio/wav", b"RIFF\x00\x00\x00\x00WAVEfictional"),
        ("audio/ogg", b"OggSfictional"),
        ("audio/webm", b"\x1aE\xdf\xa3fictional"),
    ],
)
def test_accepts_matching_file_signatures(content_type: str, content: bytes) -> None:
    validated_file = validate_upload(
        content_type=content_type,
        size_bytes=len(content),
        max_bytes=1_000,
    )

    validate_file_content(validated_file=validated_file, content=content)


def test_rejects_a_mismatched_file_signature() -> None:
    validated_file = validate_upload(
        content_type="image/png",
        size_bytes=10,
        max_bytes=1_000,
    )

    with pytest.raises(FileValidationError, match="do not match"):
        validate_file_content(validated_file=validated_file, content=b"not a png")

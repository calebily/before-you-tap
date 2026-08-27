from dataclasses import dataclass

from app.schemas import MediaKind

ALLOWED_CONTENT_TYPES: dict[str, MediaKind] = {
    "image/jpeg": MediaKind.IMAGE,
    "image/png": MediaKind.IMAGE,
    "image/webp": MediaKind.IMAGE,
    "audio/mpeg": MediaKind.AUDIO,
    "audio/mp3": MediaKind.AUDIO,
    "audio/mp4": MediaKind.AUDIO,
    "audio/m4a": MediaKind.AUDIO,
    "audio/x-m4a": MediaKind.AUDIO,
    "audio/wav": MediaKind.AUDIO,
    "audio/x-wav": MediaKind.AUDIO,
    "audio/ogg": MediaKind.AUDIO,
    "audio/webm": MediaKind.AUDIO,
}


class FileValidationError(ValueError):
    """Raised when a user-selected file is not safe to accept."""


@dataclass(frozen=True)
class ValidatedFile:
    media_kind: MediaKind
    content_type: str
    size_bytes: int


def _matches_signature(content_type: str, content: bytes) -> bool:
    if content_type == "image/jpeg":
        return content.startswith(b"\xff\xd8\xff")
    if content_type == "image/png":
        return content.startswith(b"\x89PNG\r\n\x1a\n")
    if content_type == "image/webp":
        return content.startswith(b"RIFF") and content[8:12] == b"WEBP"
    if content_type in {"audio/mpeg", "audio/mp3"}:
        return content.startswith(b"ID3") or (
            len(content) >= 2 and content[0] == 0xFF and content[1] & 0xE0 == 0xE0
        )
    if content_type in {"audio/mp4", "audio/m4a", "audio/x-m4a"}:
        return len(content) >= 12 and content[4:8] == b"ftyp"
    if content_type in {"audio/wav", "audio/x-wav"}:
        return content.startswith(b"RIFF") and content[8:12] == b"WAVE"
    if content_type == "audio/ogg":
        return content.startswith(b"OggS")
    if content_type == "audio/webm":
        return content.startswith(b"\x1aE\xdf\xa3")
    return False


def validate_upload(*, content_type: str | None, size_bytes: int, max_bytes: int) -> ValidatedFile:
    normalized_type = (content_type or "").lower().strip()
    media_kind = ALLOWED_CONTENT_TYPES.get(normalized_type)

    if media_kind is None:
        raise FileValidationError("Please choose a supported image or audio file.")
    if size_bytes <= 0:
        raise FileValidationError("The selected file is empty.")
    if size_bytes > max_bytes:
        raise FileValidationError("The selected file is too large.")

    return ValidatedFile(
        media_kind=media_kind,
        content_type=normalized_type,
        size_bytes=size_bytes,
    )


def validate_file_content(*, validated_file: ValidatedFile, content: bytes) -> None:
    if not _matches_signature(validated_file.content_type, content):
        raise FileValidationError(
            "The file contents do not match the selected image or audio file type."
        )

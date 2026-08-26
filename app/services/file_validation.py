from dataclasses import dataclass

from app.schemas import MediaKind

ALLOWED_CONTENT_TYPES: dict[str, MediaKind] = {
    "image/jpeg": MediaKind.IMAGE,
    "image/png": MediaKind.IMAGE,
    "image/webp": MediaKind.IMAGE,
    "audio/mpeg": MediaKind.AUDIO,
    "audio/mp4": MediaKind.AUDIO,
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

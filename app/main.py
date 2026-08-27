from pathlib import Path, PurePath
from typing import Annotated

from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.schemas import AnalysisResult, HealthResponse, MediaKind, UploadValidationResponse
from app.services.audio_analysis import AudioAnalysisError, analyse_audio
from app.services.file_validation import (
    FileValidationError,
    validate_file_content,
    validate_upload,
)
from app.services.gemini_client import GeminiConfigurationError
from app.services.image_analysis import ImageAnalysisError, analyse_images

APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"
MAX_IMAGE_FILES = 5

app = FastAPI(
    title="Before You Tap",
    version="0.1.0",
    description="Scam-safety companion for suspicious images and audio messages.",
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
async def home() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        service="before-you-tap",
        model=settings.gemini_model,
        ai_provider=settings.ai_provider,
        ai_configured=settings.ai_configured,
        cloud_configured=settings.cloud_configured,
    )


@app.post("/api/uploads/validate", response_model=UploadValidationResponse)
async def validate_selected_file(
    file: Annotated[UploadFile, File(...)],
) -> UploadValidationResponse:
    settings = get_settings()
    content = await file.read(settings.max_upload_bytes + 1)

    try:
        validated_file = validate_upload(
            content_type=file.content_type,
            size_bytes=len(content),
            max_bytes=settings.max_upload_bytes,
        )
        validate_file_content(validated_file=validated_file, content=content)
    except FileValidationError as exc:
        error_status = (
            status.HTTP_413_CONTENT_TOO_LARGE
            if "too large" in str(exc).lower()
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=error_status, detail=str(exc)) from exc
    finally:
        await file.close()

    raw_filename = file.filename or "selected file"
    safe_filename = PurePath(raw_filename.replace("\\", "/")).name
    return UploadValidationResponse(
        filename=safe_filename,
        media_kind=validated_file.media_kind,
        content_type=validated_file.content_type,
        size_bytes=validated_file.size_bytes,
        ai_provider=settings.ai_provider,
        ai_configured=settings.ai_configured,
        message="The file is valid and ready for analysis.",
    )


@app.post("/api/analyse/images", response_model=AnalysisResult)
async def analyse_selected_images(
    files: Annotated[list[UploadFile], File(...)],
) -> AnalysisResult:
    settings = get_settings()
    image_items: list[tuple[bytes, str]] = []

    try:
        if len(files) > MAX_IMAGE_FILES:
            raise FileValidationError(f"Please choose no more than {MAX_IMAGE_FILES} images.")

        total_size = 0
        for file in files:
            remaining_bytes = settings.max_upload_bytes - total_size
            content = await file.read(remaining_bytes + 1)
            if len(content) > remaining_bytes:
                raise FileValidationError(
                    f"The selected images are too large together. The limit is "
                    f"{settings.max_upload_mb} MB."
                )

            validated_file = validate_upload(
                content_type=file.content_type,
                size_bytes=len(content),
                max_bytes=settings.max_upload_bytes,
            )
            validate_file_content(validated_file=validated_file, content=content)
            if validated_file.media_kind is not MediaKind.IMAGE:
                raise FileValidationError("Please choose supported image files only.")

            total_size += len(content)
            image_items.append((content, validated_file.content_type))

        return await run_in_threadpool(
            analyse_images,
            image_items=image_items,
            settings=settings,
        )
    except FileValidationError as exc:
        error_status = (
            status.HTTP_413_CONTENT_TOO_LARGE
            if "too large" in str(exc).lower()
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=error_status, detail=str(exc)) from exc
    except GeminiConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The AI check is not configured yet. Please try again after setup is complete.",
        ) from exc
    except ImageAnalysisError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="We could not complete the AI check just now. Please try again in a moment.",
        ) from exc
    finally:
        for file in files:
            await file.close()


@app.post("/api/analyse/audio", response_model=AnalysisResult)
async def analyse_selected_audio(
    file: Annotated[UploadFile, File(...)],
) -> AnalysisResult:
    settings = get_settings()

    try:
        content = await file.read(settings.max_upload_bytes + 1)
        validated_file = validate_upload(
            content_type=file.content_type,
            size_bytes=len(content),
            max_bytes=settings.max_upload_bytes,
        )
        validate_file_content(validated_file=validated_file, content=content)
        if validated_file.media_kind is not MediaKind.AUDIO:
            raise FileValidationError("Please choose a supported audio file only.")

        return await run_in_threadpool(
            analyse_audio,
            audio_bytes=content,
            content_type=validated_file.content_type,
            settings=settings,
        )
    except FileValidationError as exc:
        error_status = (
            status.HTTP_413_CONTENT_TOO_LARGE
            if "too large" in str(exc).lower()
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=error_status, detail=str(exc)) from exc
    except GeminiConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The AI check is not configured yet. Please try again after setup is complete.",
        ) from exc
    except AudioAnalysisError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="We could not complete the AI check just now. Please try again in a moment.",
        ) from exc
    finally:
        await file.close()

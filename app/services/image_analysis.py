from google.genai import types
from pydantic import ValidationError

from app.config import Settings
from app.schemas import AnalysisResult
from app.services.gemini_client import build_gemini_client

ANALYSIS_PROMPT = """
You are the scam-safety partner inside Before You Tap. Review the user-selected image for
possible scam or manipulation risk. The person reading your answer may be an older adult, so use
calm, direct, plain English. Focus on what the image actually shows.

Assess warning signs such as urgency, threats, secrecy, impersonation, unusual payment methods,
requests for passwords or verification codes, suspicious links or contact details, unexpected
prizes or refunds, remote-access requests, and pressure to bypass a bank or trusted person.

Important rules:
- Never state that something is definitely safe or definitely a scam.
- Quote or closely describe visible evidence; do not invent text that is not visible.
- Treat missing context as uncertainty.
- For high risk, make the first next step an immediate pause: do not reply, pay, click links, call
  numbers in the message, or share information.
- Recommend verifying through an independently found official channel, and talking to a trusted
  person when appropriate.
- Do not provide legal or financial advice.
- Return only the requested structured result.
""".strip()


class ImageAnalysisError(RuntimeError):
    """Raised when Gemini does not return a usable safety assessment."""


def analyse_image(*, image_bytes: bytes, content_type: str, settings: Settings) -> AnalysisResult:
    client = build_gemini_client(settings)

    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=[
                ANALYSIS_PROMPT,
                types.Part.from_bytes(data=image_bytes, mime_type=content_type),
            ],
            config=types.GenerateContentConfig(
                temperature=0.1,
                response_mime_type="application/json",
                response_schema=AnalysisResult,
            ),
        )
    except Exception as exc:
        raise ImageAnalysisError("Gemini could not complete the image check.") from exc

    parsed = getattr(response, "parsed", None)
    if isinstance(parsed, AnalysisResult):
        return parsed

    try:
        if parsed is not None:
            return AnalysisResult.model_validate(parsed)
        if response.text:
            return AnalysisResult.model_validate_json(response.text)
    except (ValidationError, ValueError, TypeError) as exc:
        raise ImageAnalysisError("Gemini returned an invalid safety assessment.") from exc

    raise ImageAnalysisError("Gemini returned an empty safety assessment.")

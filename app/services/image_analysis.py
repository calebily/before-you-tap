from google.genai import types
from pydantic import ValidationError

from app.config import Settings
from app.schemas import AnalysisResult
from app.services.gemini_client import build_gemini_client

ANALYSIS_PROMPT = """
You are the scam-safety partner inside Before You Tap. Review the user-selected image pages for
possible scam or manipulation risk. The pages are supplied in the user's chosen order and are
intended to belong to the same email, conversation, or document. First check whether the visible
content actually appears continuous and related. The person reading your answer may be an older
adult, so use calm, direct, plain English. Focus on what the images actually show.

Assess warning signs such as urgency, threats, secrecy, impersonation, unusual payment methods,
requests for passwords or verification codes, suspicious links or contact details, unexpected
prizes or refunds, remote-access requests, and pressure to bypass a bank or trusted person.

Important rules:
- Never state that something is definitely safe or definitely a scam.
- Quote or closely describe visible evidence; do not invent text that is not visible.
- Treat missing context as uncertainty.
- If the pages appear to be related, consider evidence across them together.
- If the pages appear unrelated, do not combine them into one narrative. Assess each visible item
  separately, use the highest risk found as the overall risk level, and clearly say in the summary
  and uncertainty that the items may be unrelated and should be checked separately.
- For high risk, make the first next step an immediate pause: do not reply, pay, click links, call
  numbers in the message, or share information.
- Recommend verifying through an independently found official channel, and talking to a trusted
  person when appropriate.
- Choose follow_up_options only from the allowed enum values. Always include nothing_yet and
  still_unsure. Add clicked_link only when a link or button is visible; replied_or_called when a
  reply, call, or continued contact is relevant; shared_private_information when personal,
  account, password, code, or identity information is requested; and sent_money when payment or a
  transfer is requested. Return no more than five options.
- Do not provide legal or financial advice.
- Return only the requested structured result.
""".strip()


class ImageAnalysisError(RuntimeError):
    """Raised when Gemini does not return a usable safety assessment."""


def analyse_images(*, image_items: list[tuple[bytes, str]], settings: Settings) -> AnalysisResult:
    if not image_items:
        raise ImageAnalysisError("At least one image is required for analysis.")

    client = build_gemini_client(settings)

    contents: list[str | types.Part] = [ANALYSIS_PROMPT]
    for page_number, (image_bytes, content_type) in enumerate(image_items, start=1):
        contents.extend(
            [
                f"Page {page_number} of {len(image_items)}:",
                types.Part.from_bytes(data=image_bytes, mime_type=content_type),
            ]
        )

    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=contents,
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

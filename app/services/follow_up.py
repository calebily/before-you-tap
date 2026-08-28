import json

from google.genai import types
from pydantic import ValidationError

from app.config import Settings
from app.schemas import FollowUpRequest, FollowUpResult
from app.services.gemini_client import build_gemini_client

FOLLOW_UP_PROMPT = """
You are the calm safety companion inside Before You Tap. The user has already received a structured
scam-risk assessment and has pressed one controlled button describing what they have done. Give the
next safest actions for that exact situation in plain English for an older adult.

Safety rules:
- Treat the selected action as true. Do not question or shame the user.
- Never tell the user to return to a link, phone number, email address, or sender in the suspicious
  content.
- Use independently found official contact details. For banks, prefer the number on the back of the
  user's card or the official app or website typed by the user.
- If money, passwords, verification codes, banking details, identity documents, or account access
  may have been shared, make the response urgent and give concrete protective steps.
- Do not promise recovery, certainty, or legal outcomes. Do not provide legal or financial advice.
- Keep the heading short, the reassurance calm, and the next steps to four or fewer.
- Return only the requested structured result. Preserve the selected action exactly.
""".strip()


class FollowUpAnalysisError(RuntimeError):
    """Raised when Gemini does not return usable guided follow-up advice."""


def analyse_follow_up(*, request: FollowUpRequest, settings: Settings) -> FollowUpResult:
    client = build_gemini_client(settings)
    context = json.dumps(request.model_dump(mode="json"), ensure_ascii=False)

    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=[FOLLOW_UP_PROMPT, f"Existing assessment and selected action:\n{context}"],
            config=types.GenerateContentConfig(
                temperature=0.1,
                response_mime_type="application/json",
                response_schema=FollowUpResult,
            ),
        )
    except Exception as exc:
        raise FollowUpAnalysisError("Gemini could not complete the guided follow-up.") from exc

    parsed = getattr(response, "parsed", None)
    try:
        if isinstance(parsed, FollowUpResult):
            result = parsed
        elif parsed is not None:
            result = FollowUpResult.model_validate(parsed)
        elif response.text:
            result = FollowUpResult.model_validate_json(response.text)
        else:
            raise FollowUpAnalysisError("Gemini returned an empty guided follow-up.")
    except (ValidationError, ValueError, TypeError) as exc:
        raise FollowUpAnalysisError("Gemini returned invalid guided follow-up advice.") from exc

    if result.action is not request.action:
        raise FollowUpAnalysisError("Gemini changed the selected follow-up action.")
    return result

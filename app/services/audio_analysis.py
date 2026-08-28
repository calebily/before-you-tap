from google.genai import types
from pydantic import ValidationError

from app.config import Settings
from app.schemas import AnalysisResult
from app.services.gemini_client import build_gemini_client

AUDIO_ANALYSIS_PROMPT = """
You are the scam-safety partner inside Before You Tap. Review the user-selected saved voicemail,
voice message, or audio file for possible scam or manipulation risk. The person reading your answer
may be an older adult, so use calm, direct, plain English. Focus on what is actually audible.

Assess warning signs such as urgency, threats, secrecy, impersonation, unusual payment methods,
requests for passwords, verification codes, banking or identity details, suspicious callback
instructions, unexpected prizes or refunds, remote-access requests, and pressure to bypass a bank,
family member, or trusted person.

Important rules:
- Never state that something is definitely safe or definitely a scam.
- Quote or closely paraphrase audible evidence; do not invent speech that is unclear or inaudible.
- Treat missing context, unclear audio, unknown speakers, and uncertain language as uncertainty.
- For high risk, make the first next step an immediate pause: do not call a supplied number, reply,
  pay, follow instructions, install software, or share information.
- Recommend verifying through an independently found official channel, and talking to a trusted
  person when appropriate.
- Choose follow_up_options only from the allowed enum values. Always include nothing_yet and
  still_unsure. Add clicked_link only when the recording directs the listener to a link;
  replied_or_called when a reply, callback, or continued contact is relevant;
  shared_private_information when personal, account, password, code, or identity information is
  requested; and sent_money when payment or a transfer is requested. Return no more than five
  options.
- Do not provide legal or financial advice.
- Return only the requested structured result.
""".strip()


class AudioAnalysisError(RuntimeError):
    """Raised when Gemini does not return a usable audio safety assessment."""


def _gemini_mime_type(content_type: str) -> str:
    aliases = {
        "audio/x-m4a": "audio/m4a",
        "audio/x-wav": "audio/wav",
    }
    return aliases.get(content_type, content_type)


def analyse_audio(*, audio_bytes: bytes, content_type: str, settings: Settings) -> AnalysisResult:
    if not audio_bytes:
        raise AudioAnalysisError("An audio file is required for analysis.")

    client = build_gemini_client(settings)
    contents: list[str | types.Part] = [
        AUDIO_ANALYSIS_PROMPT,
        types.Part.from_bytes(
            data=audio_bytes,
            mime_type=_gemini_mime_type(content_type),
        ),
    ]

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
        raise AudioAnalysisError("Gemini could not complete the audio check.") from exc

    parsed = getattr(response, "parsed", None)
    if isinstance(parsed, AnalysisResult):
        return parsed

    try:
        if parsed is not None:
            return AnalysisResult.model_validate(parsed)
        if response.text:
            return AnalysisResult.model_validate_json(response.text)
    except (ValidationError, ValueError, TypeError) as exc:
        raise AudioAnalysisError("Gemini returned an invalid safety assessment.") from exc

    raise AudioAnalysisError("Gemini returned an empty safety assessment.")

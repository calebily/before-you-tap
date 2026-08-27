from google import genai

from app.config import Settings


class GeminiConfigurationError(RuntimeError):
    """Raised when neither a free API key nor Vertex AI is configured."""


def build_gemini_client(settings: Settings) -> genai.Client:
    if settings.google_genai_use_vertexai:
        if not settings.google_cloud_project:
            raise GeminiConfigurationError(
                "GOOGLE_CLOUD_PROJECT is required when Vertex AI is enabled."
            )
        return genai.Client(
            vertexai=True,
            project=settings.google_cloud_project,
            location=settings.google_cloud_location,
        )

    if not settings.google_api_key:
        raise GeminiConfigurationError(
            "GOOGLE_API_KEY is required for Google AI Studio development."
        )
    return genai.Client(api_key=settings.google_api_key.get_secret_value())

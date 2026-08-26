from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    google_cloud_project: str | None = None
    google_cloud_location: str = "global"
    google_genai_use_vertexai: bool = False
    google_api_key: SecretStr | None = None
    gemini_model: str = "gemini-3.5-flash"
    max_upload_mb: int = 20

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_mb * 1024 * 1024

    @property
    def cloud_configured(self) -> bool:
        return bool(self.google_cloud_project)

    @property
    def ai_provider(self) -> str:
        return "vertex_ai" if self.google_genai_use_vertexai else "google_ai_studio"

    @property
    def ai_configured(self) -> bool:
        if self.google_genai_use_vertexai:
            return self.cloud_configured
        return bool(self.google_api_key and self.google_api_key.get_secret_value())


@lru_cache
def get_settings() -> Settings:
    return Settings()

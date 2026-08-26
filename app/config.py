from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    google_cloud_project: str | None = None
    google_cloud_location: str = "global"
    google_genai_use_enterprise: bool = True
    gemini_model: str = "gemini-3.5-flash"
    max_upload_mb: int = 20

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_mb * 1024 * 1024

    @property
    def cloud_configured(self) -> bool:
        return bool(self.google_cloud_project)


@lru_cache
def get_settings() -> Settings:
    return Settings()

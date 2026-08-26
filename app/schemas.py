from enum import StrEnum

from pydantic import BaseModel, Field


class MediaKind(StrEnum):
    IMAGE = "image"
    AUDIO = "audio"


class RiskLevel(StrEnum):
    LOW_CONCERN = "low_concern"
    BE_CAREFUL = "be_careful"
    HIGH_RISK = "high_risk"


class WarningSign(BaseModel):
    title: str
    evidence: str
    explanation: str


class AnalysisResult(BaseModel):
    risk_level: RiskLevel
    summary: str
    warning_signs: list[WarningSign] = Field(default_factory=list)
    uncertainty: list[str] = Field(default_factory=list)
    safe_next_steps: list[str] = Field(min_length=1, max_length=3)


class HealthResponse(BaseModel):
    status: str
    service: str
    model: str
    cloud_configured: bool

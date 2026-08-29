from enum import StrEnum

from pydantic import BaseModel, Field, model_validator


class MediaKind(StrEnum):
    IMAGE = "image"
    AUDIO = "audio"


class RiskLevel(StrEnum):
    LOW_CONCERN = "low_concern"
    BE_CAREFUL = "be_careful"
    HIGH_RISK = "high_risk"


class FollowUpAction(StrEnum):
    NOTHING_YET = "nothing_yet"
    CLICKED_LINK = "clicked_link"
    REPLIED_OR_CALLED = "replied_or_called"
    SHARED_PRIVATE_INFORMATION = "shared_private_information"
    SENT_MONEY = "sent_money"
    STILL_UNSURE = "still_unsure"


class WarningSign(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    evidence: str = Field(min_length=1, max_length=240)
    explanation: str = Field(min_length=1, max_length=320)


class LowConcernReason(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    evidence: str = Field(min_length=1, max_length=240)
    explanation: str = Field(min_length=1, max_length=320)


class AnalysisResult(BaseModel):
    risk_level: RiskLevel
    summary: str = Field(min_length=1, max_length=360)
    warning_signs: list[WarningSign] = Field(default_factory=list, max_length=5)
    low_concern_reasons: list[LowConcernReason] = Field(default_factory=list, max_length=3)
    uncertainty: list[str] = Field(default_factory=list, max_length=3)
    safe_next_steps: list[str] = Field(min_length=1, max_length=3)
    follow_up_options: list[FollowUpAction] = Field(
        default_factory=lambda: [FollowUpAction.NOTHING_YET, FollowUpAction.STILL_UNSURE],
        min_length=1,
        max_length=5,
    )

    @model_validator(mode="after")
    def keep_low_concern_reasoning_visible(self) -> "AnalysisResult":
        if self.risk_level is RiskLevel.LOW_CONCERN and not self.low_concern_reasons:
            self.low_concern_reasons = [
                LowConcernReason(
                    title="No strong warning signs found",
                    evidence=self.summary[:240],
                    explanation=(
                        "This supports a Low concern result, but it does not confirm the sender "
                        "or guarantee that the message is safe."
                    ),
                )
            ]
        elif self.risk_level is not RiskLevel.LOW_CONCERN:
            self.low_concern_reasons = []
        return self


class FollowUpRequest(BaseModel):
    action: FollowUpAction
    analysis: AnalysisResult


class FollowUpResult(BaseModel):
    action: FollowUpAction
    heading: str = Field(min_length=1, max_length=100)
    reassurance: str = Field(min_length=1, max_length=280)
    next_steps: list[str] = Field(min_length=1, max_length=4)
    urgent_note: str = Field(default="", max_length=240)


class HealthResponse(BaseModel):
    status: str
    service: str
    model: str
    ai_provider: str
    ai_configured: bool
    cloud_configured: bool


class UploadValidationResponse(BaseModel):
    filename: str
    media_kind: MediaKind
    content_type: str
    size_bytes: int
    ai_provider: str
    ai_configured: bool
    message: str

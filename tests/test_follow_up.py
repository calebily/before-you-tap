from types import SimpleNamespace

import pytest

from app.config import Settings
from app.schemas import (
    AnalysisResult,
    FollowUpAction,
    FollowUpRequest,
    FollowUpResult,
    RiskLevel,
)
from app.services import follow_up


def _request() -> FollowUpRequest:
    return FollowUpRequest(
        action=FollowUpAction.SENT_MONEY,
        analysis=AnalysisResult(
            risk_level=RiskLevel.HIGH_RISK,
            summary="The caller pressured the listener to transfer money.",
            warning_signs=[],
            uncertainty=["The caller's identity cannot be confirmed."],
            safe_next_steps=["Pause and contact the bank using an official number."],
            follow_up_options=[
                FollowUpAction.NOTHING_YET,
                FollowUpAction.SENT_MONEY,
                FollowUpAction.STILL_UNSURE,
            ],
        ),
    )


def test_builds_a_structured_follow_up_request_without_resending_media(monkeypatch) -> None:
    request = _request()
    expected = FollowUpResult(
        action=FollowUpAction.SENT_MONEY,
        heading="Call the bank now",
        reassurance="Acting quickly may help protect the account.",
        next_steps=[
            "Call the bank using the number on the back of your card.",
            "Tell the bank's fraud team what happened.",
            "Save the payment record and messages.",
        ],
        urgent_note="Do not contact the person who requested the payment again.",
    )
    calls = {}

    class FakeModels:
        def generate_content(self, **kwargs):
            calls.update(kwargs)
            return SimpleNamespace(parsed=expected, text=None)

    monkeypatch.setattr(
        follow_up,
        "build_gemini_client",
        lambda settings: SimpleNamespace(models=FakeModels()),
    )
    settings = Settings(
        _env_file=None,
        google_genai_use_vertexai=True,
        google_cloud_project="fictional-project",
    )

    result = follow_up.analyse_follow_up(request=request, settings=settings)

    assert result == expected
    assert calls["model"] == "gemini-3.5-flash"
    assert len(calls["contents"]) == 2
    assert "sent_money" in calls["contents"][1]
    assert "The caller pressured" in calls["contents"][1]
    assert not any(hasattr(item, "inline_data") for item in calls["contents"])
    assert calls["config"].response_mime_type == "application/json"


def test_rejects_a_response_that_changes_the_selected_action(monkeypatch) -> None:
    request = _request()
    wrong_action = FollowUpResult(
        action=FollowUpAction.NOTHING_YET,
        heading="Pause first",
        reassurance="Take a moment before doing anything else.",
        next_steps=["Contact the organisation through an official channel."],
    )

    class FakeModels:
        def generate_content(self, **kwargs):
            return SimpleNamespace(parsed=wrong_action, text=None)

    monkeypatch.setattr(
        follow_up,
        "build_gemini_client",
        lambda settings: SimpleNamespace(models=FakeModels()),
    )

    with pytest.raises(follow_up.FollowUpAnalysisError, match="changed"):
        follow_up.analyse_follow_up(request=request, settings=Settings(_env_file=None))

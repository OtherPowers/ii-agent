import pytest

from otherpowers_governance.signals.api import new_signal
from otherpowers_governance.signals.schema import (
    Posture,
    Uncertainty,
    IntelligenceMode,
    WithholdReason,
)


def test_new_signal_returns_plain_mapping():
    sig = new_signal(
        posture=Posture.OPEN,
        uncertainty=Uncertainty.HIGH,
        mode=IntelligenceMode.COLLABORATIVE,
        withhold=WithholdReason.NONE,
    )

    assert isinstance(sig, dict)


def test_new_signal_is_sparse_and_non_coercive():
    sig = new_signal(posture=Posture.OPEN)

    # Only explicitly provided fields appear
    assert sig == {"posture": "open"}


def test_new_signal_allows_payload_without_interpretation():
    payload = {"gradient": {"trust": "emergent"}}

    sig = new_signal(payload=payload)

    assert sig["payload"] == payload


def test_new_signal_does_not_inject_defaults():
    sig = new_signal()

    assert sig == {}


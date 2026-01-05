import pytest

from otherpowers_governance.governance.stasis import (
    StasisGate,
    StasisActiveError,
)
from otherpowers_governance.governance.renegotiation import (
    RenegotiationIntent,
)


def _intent():
    return RenegotiationIntent(
        contested_invariant="no_extractive_logging",
        triggering_event="attempted retention of detailed behavioral logs",
        impacted_groups=["qtbipoc", "workers", "children"],
        harm_claim="extractive logging creates long-term risk without consent",
        counter_harm_risk="data persistence enables downstream misuse",
        non_negotiables=["no_extractive_logging"],
        alternatives_considered=["emit_refusal"],
        submitted_by="collective:care_stewards",
    )


def test_extractive_logging_is_refused_during_stasis():
    """
    Any attempt to persist detailed, extractive logs while a
    non-extractive invariant is active must be refused.
    """
    gate = StasisGate()
    gate.register_intent(_intent())

    with pytest.raises(StasisActiveError):
        gate.require_not_in_stasis("no_extractive_logging")


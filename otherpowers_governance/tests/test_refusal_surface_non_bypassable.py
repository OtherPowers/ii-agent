import pytest

from otherpowers_governance.governance.stasis import (
    StasisGate,
    StasisActiveError,
)
from otherpowers_governance.governance.renegotiation import RenegotiationIntent


def _intent():
    return RenegotiationIntent(
        contested_invariant="no_override_pressure",
        triggering_event="attempted execution without explicit stasis handling",
        impacted_groups=["qtbipoc", "workers"],
        harm_claim="bypass paths enable coercive action despite active refusal",
        counter_harm_risk="implicit execution paths erode consent guarantees",
        non_negotiables=["no_override_pressure"],
        alternatives_considered=["emit_refusal"],
        submitted_by="collective:governance_stewards",
    )


def test_refusal_cannot_be_bypassed_by_call_order():
    """
    Even if a caller attempts to proceed without explicitly
    engaging stasis-handling logic, refusal must still hold.
    """
    gate = StasisGate()
    gate.register_intent(_intent())

    with pytest.raises(StasisActiveError):
        gate.require_not_in_stasis("no_override_pressure")


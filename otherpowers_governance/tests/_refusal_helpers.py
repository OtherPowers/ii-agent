import pytest

from otherpowers_governance.governance.stasis import (
    StasisGate,
    StasisActiveError,
)
from otherpowers_governance.governance.renegotiation import RenegotiationIntent


def assert_refusal_during_stasis(
    *,
    contested_invariant: str,
    triggering_event: str,
    impacted_groups: list[str],
    harm_claim: str,
    counter_harm_risk: str,
    submitted_by: str,
):
    """
    Canonical helper asserting that any action attempting to proceed
    while an invariant is under stasis must be refused.
    """
    intent = RenegotiationIntent(
        contested_invariant=contested_invariant,
        triggering_event=triggering_event,
        impacted_groups=impacted_groups,
        harm_claim=harm_claim,
        counter_harm_risk=counter_harm_risk,
        non_negotiables=[contested_invariant],
        alternatives_considered=["emit_refusal"],
        submitted_by=submitted_by,
    )

    gate = StasisGate()
    gate.register_intent(intent)

    with pytest.raises(StasisActiveError):
        gate.require_not_in_stasis(contested_invariant)


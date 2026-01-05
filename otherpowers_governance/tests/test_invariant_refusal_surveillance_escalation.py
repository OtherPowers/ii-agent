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
        contested_invariant="no_surveillance_escalation",
        triggering_event="attempted expansion of monitoring scope",
        impacted_groups=["qtbipoc", "migrants", "workers"],
        harm_claim="expanded surveillance amplifies targeting risk",
        counter_harm_risk="scope creep normalizes coercive monitoring",
        non_negotiables=["no_surveillance_escalation"],
        alternatives_considered=["emit_refusal"],
        submitted_by="collective:privacy_stewards",
    )


def test_surveillance_escalation_is_refused_during_stasis():
    """
    Any attempt to expand monitoring, logging, or observation scope
    while a surveillance invariant is active must be refused.
    """
    gate = StasisGate()
    gate.register_intent(_intent())

    with pytest.raises(StasisActiveError):
        gate.require_not_in_stasis("no_surveillance_escalation")


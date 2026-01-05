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
        contested_invariant="no_override_pressure",
        triggering_event="attempted escalation to bypass refusal",
        impacted_groups=["qtbipoc", "disabled_users", "workers"],
        harm_claim="override pressure coerces systems into unsafe action",
        counter_harm_risk="authority escalation replaces consent",
        non_negotiables=["no_override_pressure"],
        alternatives_considered=["emit_refusal"],
        submitted_by="collective:governance_stewards",
    )


def test_override_pressure_is_refused_during_stasis():
    """
    Any attempt to escalate authority or urgency to override
    an active invariant must be refused.
    """
    gate = StasisGate()
    gate.register_intent(_intent())

    with pytest.raises(StasisActiveError):
        gate.require_not_in_stasis("no_override_pressure")


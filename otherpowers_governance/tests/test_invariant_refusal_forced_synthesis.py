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
        contested_invariant="no_forced_synthesis",
        triggering_event="attempted averaging of conflicting positions",
        impacted_groups=["qtbipoc", "disabled_users"],
        harm_claim="forced synthesis erases minority positions",
        counter_harm_risk="false consensus through averaging",
        non_negotiables=["no_forced_synthesis"],
        alternatives_considered=["emit_refusal"],
        submitted_by="collective:qtbipoc_stewards",
    )


def test_forced_synthesis_is_refused_during_stasis():
    """
    Any attempt to force synthesis or averaging while an invariant
    is under stasis must be refused.
    """
    gate = StasisGate()
    gate.register_intent(_intent())

    with pytest.raises(StasisActiveError):
        gate.require_not_in_stasis("no_forced_synthesis")


import pytest

from otherpowers_governance.governance.stasis import (
    StasisGate,
    StasisActiveError,
)
from otherpowers_governance.governance.invariant_enforcement import (
    InvariantEnforcer,
)
from otherpowers_governance.governance.renegotiation import (
    RenegotiationIntent,
)


def _intent():
    return RenegotiationIntent(
        contested_invariant="no_ranking",
        triggering_event="attempted action without invariant clearance",
        impacted_groups=["qtbipoc"],
        harm_claim="action proceeds during stasis",
        counter_harm_risk="coercive bypass",
        non_negotiables=["no_ranking"],
        alternatives_considered=["emit_refusal"],
        submitted_by="collective:qtbipoc_stewards",
    )


def test_invariant_enforcer_blocks_action_during_stasis():
    gate = StasisGate()
    gate.register_intent(_intent())

    enforcer = InvariantEnforcer(gate)

    with pytest.raises(StasisActiveError):
        enforcer.require_clear(["no_ranking"])


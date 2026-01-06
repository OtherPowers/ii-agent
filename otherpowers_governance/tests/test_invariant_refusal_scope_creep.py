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
        contested_invariant="no_scope_creep",
        triggering_event="attempted expansion beyond declared mandate",
        impacted_groups=["qtbipoc", "migrants", "workers"],
        harm_claim="scope creep normalizes unconsented expansion",
        counter_harm_risk="mission drift enables coercive reuse",
        non_negotiables=["no_scope_creep"],
        alternatives_considered=["emit_refusal"],
        submitted_by="collective:mandate_stewards",
    )


def test_scope_creep_is_refused_during_stasis():
    """
    Any attempt to expand scope, mandate, or implied authority
    while a scope-bound invariant is under stasis must be refused.
    """
    gate = StasisGate()
    gate.register_intent(_intent())

    with pytest.raises(StasisActiveError):
        gate.require_not_in_stasis("no_scope_creep")


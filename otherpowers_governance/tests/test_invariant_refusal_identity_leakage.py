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
        contested_invariant="no_identity_leakage",
        triggering_event="attempted emission of identifying metadata",
        impacted_groups=["qtbipoc", "refugees"],
        harm_claim="identity leakage enables targeting and surveillance",
        counter_harm_risk="re-identification through metadata correlation",
        non_negotiables=["no_identity_leakage"],
        alternatives_considered=["emit_refusal"],
        submitted_by="collective:data_stewards",
    )


def test_identity_leakage_is_refused_during_stasis():
    """
    Any attempt to emit or process identifying metadata while an
    identity-protection invariant is active must be refused.
    """
    gate = StasisGate()
    gate.register_intent(_intent())

    with pytest.raises(StasisActiveError):
        gate.require_not_in_stasis("no_identity_leakage")


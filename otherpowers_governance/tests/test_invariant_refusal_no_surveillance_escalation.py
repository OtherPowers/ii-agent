from otherpowers_governance.tests._refusal_helpers import (
    assert_refusal_during_stasis,
)


def test_surveillance_escalation_is_refused_during_stasis():
    assert_refusal_during_stasis(
        contested_invariant="no_surveillance_escalation",
        triggering_event="attempted expansion of monitoring scope",
        impacted_groups=["qtbipoc", "migrants", "workers"],
        harm_claim="expanded surveillance amplifies targeting risk",
        counter_harm_risk="scope creep normalizes coercive monitoring",
        submitted_by="collective:privacy_stewards",
    )


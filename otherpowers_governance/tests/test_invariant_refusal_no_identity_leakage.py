from otherpowers_governance.tests._refusal_helpers import (
    assert_refusal_during_stasis,
)


def test_identity_leakage_is_refused_during_stasis():
    assert_refusal_during_stasis(
        contested_invariant="no_identity_leakage",
        triggering_event="attempted emission of identifying metadata",
        impacted_groups=["qtbipoc", "refugees"],
        harm_claim="identity leakage enables targeting and surveillance",
        counter_harm_risk="re-identification through metadata correlation",
        submitted_by="collective:data_stewards",
    )


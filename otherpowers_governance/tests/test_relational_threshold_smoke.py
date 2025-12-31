from otherpowers_governance.governance.stasis import (
    RelationalThreshold,
    StasisEncountered,
    InvalidResolutionError,
)
from otherpowers_governance.governance.renegotiation import (
    RenegotiationIntent,
    RenegotiationResolution,
)


def _intent():
    return RenegotiationIntent(
        contested_invariant="no_ranking",
        triggering_event="attempted ranking",
        situated_context="access harm reported",
        impacted_groups=["qtbipoc", "disabled_users"],
        harm_claim="ranking blocks access",
        counter_harm_risk="comparative gradients",
        non_negotiables=["no_ranking"],
        alternatives_considered=["emit_refusal"],
        submitted_by="collective:qtbipoc_stewards",
    )


def _resolution(contested_invariant: str):
    return RenegotiationResolution(
        contested_invariant=contested_invariant,
        summary="Community review completed with consensus to resolve stasis.",
        community_window_closed=True,
        alt_modality_trace="non-comparative harm buffer pathway used",
        quorum_attestations=[
            "council:access_review_circle",
            "guild:implementation_stewards",
        ],
    )


def test_encounter_raises_stasis_with_context():
    threshold = RelationalThreshold()
    intent = _intent()

    threshold.hold_space(intent)

    try:
        threshold.encounter("no_ranking")
        assert False, "Expected StasisEncountered"
    except StasisEncountered as e:
        assert e.intent == intent
        assert "Resolution Context" in str(e)


def test_stay_with_trouble_returns_intent():
    threshold = RelationalThreshold()
    intent = _intent()

    threshold.hold_space(intent)

    returned = threshold.stay_with_trouble("no_ranking")
    assert returned == intent


def test_acknowledge_resolution_clears_stasis():
    threshold = RelationalThreshold()
    intent = _intent()
    resolution = _resolution("no_ranking")

    threshold.hold_space(intent)
    threshold.acknowledge_resolution(resolution)

    assert not threshold.is_stasis_tended("no_ranking")


def test_invalid_resolution_mismatch_raises():
    threshold = RelationalThreshold()
    intent = _intent()

    threshold.hold_space(intent)

    bad_resolution = _resolution("different_invariant")

    try:
        threshold.acknowledge_resolution(bad_resolution)
        assert False, "Expected InvalidResolutionError"
    except InvalidResolutionError:
        pass


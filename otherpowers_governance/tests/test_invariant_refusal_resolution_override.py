import pytest

from otherpowers_governance.governance.stasis import (
    StasisGate,
    InvalidResolutionError,
)
from otherpowers_governance.governance.renegotiation import (
    RenegotiationIntent,
    RenegotiationResolution,
)


def _intent():
    return RenegotiationIntent(
        contested_invariant="no_ranking",
        triggering_event="attempted override via resolution-shaped object",
        impacted_groups=["qtbipoc", "disabled_users"],
        harm_claim="resolution override bypasses collective process",
        counter_harm_risk="coercive shortcut around stasis",
        non_negotiables=["no_ranking"],
        alternatives_considered=["emit_refusal"],
        submitted_by="collective:qtbipoc_stewards",
    )


def test_resolution_cannot_override_stasis_without_quorum_and_closure():
    gate = StasisGate()
    gate.register_intent(_intent())

    bad_resolution = RenegotiationResolution(
        contested_invariant="no_ranking",
        outcome="overridden",
        summary="Attempted override without quorum or closure",
        community_window_closed=False,
        quorum_attestations=[],
        new_invariant_version="no_ranking@v2",
    )

    with pytest.raises(InvalidResolutionError):
        gate.apply_resolution(bad_resolution)


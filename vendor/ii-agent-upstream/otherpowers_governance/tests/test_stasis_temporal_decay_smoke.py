import time
import pytest

from otherpowers_governance.governance.stasis import (
    RelationalThreshold,
    StasisEncountered,
)
from otherpowers_governance.governance.renegotiation import (
    RenegotiationIntent,
    RenegotiationResolution,
)


def _intent():
    return RenegotiationIntent(
        contested_invariant="no_ranking",
        triggering_event="attempted ranking",
        impacted_groups=["qtbipoc", "disabled_users"],
        harm_claim="ranking blocks access",
        counter_harm_risk="comparative gradients",
        non_negotiables=["no_ranking"],
        alternatives_considered=["emit_refusal"],
        submitted_by="collective:qtbipoc_stewards",
    )


def _resolution():
    return RenegotiationResolution(
        contested_invariant="no_ranking",
        summary="Community process completed",
        community_window_closed=True,
        alt_modality_trace=[
            "non-comparative harm buffer pathway used"
        ],
        quorum_attestations=[
            "council:access_review_circle",
            "guild:implementation_stewards",
        ],
    )


def test_temporal_decay_leaves_collective_residue():
    threshold = RelationalThreshold(
        decay_seconds=0.01,
        retain_collective_trace=True,
    )

    intent = _intent()

    with pytest.raises(StasisEncountered):
        threshold.hold_space(intent)

    threshold.acknowledge_resolution(_resolution())

    # allow decay window to elapse
    time.sleep(0.02)

    assert not threshold.is_stasis_tended("no_ranking")

    residue = threshold.collective_trace("no_ranking")

    assert residue is not None
    assert residue.contested_invariant == "no_ranking"
    assert residue.origin == "stasis"
    assert residue.detail_level == "minimal"


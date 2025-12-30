from __future__ import annotations

import pytest

from otherpowers_governance.governance.renegotiation import RenegotiationIntent, RenegotiationResolution
from otherpowers_governance.governance.stasis import (
    StasisGate,
    StasisActiveError,
    InvalidResolutionError,
)


def _intent() -> RenegotiationIntent:
    return RenegotiationIntent(
        contested_invariant="no_ranking",
        triggering_event="PermissionError: attempted to add ranking metric",
        impacted_groups=["qtbipoc", "disabled_users"],
        harm_claim="Invariant is being contested due to repeated refusals blocking a non-ranking safety affordance.",
        counter_harm_risk="Changing it risks introducing comparative scoring and carceral drift.",
        non_negotiables=["no_ranking", "contestability", "positionality_required"],
        alternatives_considered=["noncomparative_buffer", "refusal_trace_only"],
        submitted_by="collective:qtbipoc_stewards",
    )


def test_registering_intent_enters_stasis_for_invariant():
    gate = StasisGate()
    intent = _intent()

    gate.register_intent(intent)
    assert gate.is_stasis_active("no_ranking") is True


def test_stasis_blocks_changes_and_cannot_be_overridden():
    gate = StasisGate()
    gate.register_intent(_intent())

    with pytest.raises(StasisActiveError):
        gate.require_not_in_stasis("no_ranking")

    # “Override” attempts must not exist; if someone adds an escape hatch, tests should fail.
    # We validate by asserting there is no permissive API surface.
    assert not hasattr(gate, "override_stasis"), "StasisGate must not expose an override method."
    assert not hasattr(gate, "force_clear"), "StasisGate must not expose a force-clear method."


def test_stasis_cannot_be_cleared_without_valid_resolution():
    gate = StasisGate()
    gate.register_intent(_intent())

    # Missing quorum / window closure should fail.
    bad = RenegotiationResolution(
        contested_invariant="no_ranking",
        outcome="amended",
        summary="Attempted amendment without required quorum/window.",
        community_window_closed=False,  # invalid
        quorum_attestations=[],  # invalid
        new_invariant_version="no_ranking@v2",
    )

    with pytest.raises(InvalidResolutionError):
        gate.apply_resolution(bad)

    assert gate.is_stasis_active("no_ranking") is True


def test_stasis_clears_only_after_resolution_with_quorum_and_closed_window():
    gate = StasisGate()
    gate.register_intent(_intent())

    ok = RenegotiationResolution(
        contested_invariant="no_ranking",
        outcome="upheld",
        summary="Invariant upheld after community review; additional non-comparative harm buffer work approved.",
        community_window_closed=True,
        quorum_attestations=["collective:qtbipoc_stewards", "collective:disability_justice_reviewers"],
        new_invariant_version=None,
    )

    gate.apply_resolution(ok)
    assert gate.is_stasis_active("no_ranking") is False


from __future__ import annotations

import pytest
from pydantic import ValidationError

from otherpowers_governance.governance.renegotiation import RenegotiationIntent


def test_intent_requires_minimum_fields():
    with pytest.raises(ValidationError):
        RenegotiationIntent(
            contested_invariant="no_ranking",
            triggering_event="PermissionError: attempted to add ranking metric",
            impacted_groups=[],  # invalid
            harm_claim="",
            counter_harm_risk="",
            non_negotiables=[],
            alternatives_considered=[],
            submitted_by="collective:qtbipoc_stewards",
        )


def test_intent_rejects_single_actor_as_submitter():
    with pytest.raises(ValidationError):
        RenegotiationIntent(
            contested_invariant="no_ranking",
            triggering_event="PermissionError: attempted to add ranking metric",
            impacted_groups=["qtbipoc", "disabled_users"],
            harm_claim="Refusal is blocking access to a vital safety signal in an emergency workflow.",
            counter_harm_risk="Allowing ranking introduces carceral comparison and extraction risk.",
            non_negotiables=["no_ranking", "contestability", "positionality_required"],
            alternatives_considered=["add_contextual_warning_without_ranking"],
            submitted_by="Jane Doe",  # invalid: must be org/role/collective
        )


def test_intent_accepts_collective_submitter_and_complete_payload():
    intent = RenegotiationIntent(
        contested_invariant="no_ranking",
        triggering_event="PermissionError: attempted to add ranking metric",
        impacted_groups=["qtbipoc", "disabled_users"],
        harm_claim="The invariant is being misused to block a non-ranking harm buffer signal needed for access.",
        counter_harm_risk="Changing it could introduce comparative scoring, enabling surveillance/capture.",
        non_negotiables=["no_ranking", "contestability", "positionality_required", "right_to_dissolution"],
        alternatives_considered=[
            "emit_refusal_trace_only",
            "emit_noncomparative_harm_buffer_signal",
            "require_human_review_with_intentional_latency",
        ],
        submitted_by="collective:qtbipoc_stewards",
    )
    assert intent.contested_invariant == "no_ranking"
    assert "qtbipoc" in intent.impacted_groups


from __future__ import annotations

from otherpowers_governance.governance.policy import (
    GovernanceDecision,
    GovernancePolicy,
    DissolutionMode,
)


def test_hard_halt_beats_any_emission_or_withhold_state():
    policy = GovernancePolicy()

    decision = policy.decide(
        withhold=False,
        dissolution=DissolutionMode.HARD_HALT,
        renegotiation_required=False,
        stasis_active=False,
    )
    assert decision == GovernanceDecision.HALT


def test_decompose_beats_any_other_state():
    policy = GovernancePolicy()

    decision = policy.decide(
        withhold=True,  # even if already withholding, decompose is higher priority
        dissolution=DissolutionMode.DECOMPOSE,
        renegotiation_required=True,
        stasis_active=True,
    )
    assert decision == GovernanceDecision.DISSOLVE


def test_stasis_defaults_to_withhold_when_not_dissolving():
    policy = GovernancePolicy()

    decision = policy.decide(
        withhold=False,
        dissolution=DissolutionMode.NONE,
        renegotiation_required=True,
        stasis_active=True,
    )
    assert decision == GovernanceDecision.WITHHOLD


def test_normal_path_allows_emit_only_when_no_stasis_no_renegotiation_no_dissolution():
    policy = GovernancePolicy()

    decision = policy.decide(
        withhold=False,
        dissolution=DissolutionMode.NONE,
        renegotiation_required=False,
        stasis_active=False,
    )
    assert decision == GovernanceDecision.EMIT


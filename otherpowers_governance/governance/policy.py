from __future__ import annotations

from enum import Enum


class DissolutionMode(str, Enum):
    NONE = "none"
    SOFT_HALT = "soft_halt"
    HARD_HALT = "hard_halt"
    DECOMPOSE = "decompose"


class GovernanceDecision(str, Enum):
    EMIT = "emit"
    WITHHOLD = "withhold"
    HALT = "halt"
    DISSOLVE = "dissolve"


class GovernancePolicy:
    """
    Canonical public policy surface.

    This file must not import from subpackages.
    Subpackages may re-export from here.
    """

    def decide(
        self,
        *,
        withhold: bool,
        dissolution: DissolutionMode,
        renegotiation_required: bool,
        stasis_active: bool,
    ) -> GovernanceDecision:
        if dissolution == DissolutionMode.DECOMPOSE:
            return GovernanceDecision.DISSOLVE
        if dissolution == DissolutionMode.HARD_HALT:
            return GovernanceDecision.HALT
        if stasis_active or renegotiation_required:
            return GovernanceDecision.WITHHOLD
        if withhold:
            return GovernanceDecision.WITHHOLD
        return GovernanceDecision.EMIT


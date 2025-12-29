"""
Signals package.

Canonical signal schemas and accumulators.
Explicit exports only. No implicit re-export magic.
"""

from .schema import (
    Posture,
    Uncertainty,
    IntelligenceMode,
    WithholdReason,
    GovernanceDecision,
    SignalEnvelope,
)

from .accumulator import GovernanceAccumulator
from .posture_accumulator import PostureAccumulator

__all__ = [
    "Posture",
    "Uncertainty",
    "IntelligenceMode",
    "WithholdReason",
    "GovernanceDecision",
    "SignalEnvelope",
    "GovernanceAccumulator",
    "PostureAccumulator",
]


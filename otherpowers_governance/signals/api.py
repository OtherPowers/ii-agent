"""
Public Signals API.

This module is the ONLY supported construction surface
for governance-safe signals.
"""

from typing import Mapping

from otherpowers_governance.signals.schema import (
    Posture,
    Uncertainty,
    IntelligenceMode,
    WithholdReason,
)


def new_signal(
    *,
    posture: Posture,
    uncertainty: Uncertainty,
    mode: IntelligenceMode,
    withhold: WithholdReason,
) -> Mapping:
    """
    Canonical constructor for governance signals.

    Returns a plain mapping to preserve:
    - serialization safety
    - testability
    - non-coercive boundaries
    """
    return {
        "posture": posture.value,
        "uncertainty": uncertainty.value,
        "mode": mode.value,
        "withhold": withhold.value,
    }


__all__ = [
    "new_signal",
]


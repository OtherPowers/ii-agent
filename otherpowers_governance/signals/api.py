"""
Public, stable API for OtherPowers.co Creative Intelligence.

This module is the ONLY supported construction surface
for governance-safe signals.
"""

from __future__ import annotations

from typing import Mapping, Optional

from otherpowers_governance.signals.schema import (
    Posture,
    Uncertainty,
    IntelligenceMode,
    WithholdReason,
)


def new_signal(
    *,
    posture: Optional[Posture] = None,
    uncertainty: Optional[Uncertainty] = None,
    mode: Optional[IntelligenceMode] = None,
    withhold: Optional[WithholdReason] = None,
    payload: Optional[dict] = None,
) -> Mapping:
    """
    Canonical constructor for governance signals.

    Returns a plain mapping to preserve:
    - serialization safety
    - testability
    - non-coercive boundaries
    """
    signal: dict = {}

    if payload is not None:
        signal["payload"] = payload

    if posture is not None:
        signal["posture"] = posture.value

    if uncertainty is not None:
        signal["uncertainty"] = uncertainty.value

    if mode is not None:
        signal["mode"] = mode.value

    if withhold is not None:
        signal["withhold"] = withhold.value

    return signal


__all__ = ["new_signal"]


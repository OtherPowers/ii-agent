# otherpowers_governance/__init__.py
#
# Root package for OtherPowers governance framework.
# This file intentionally avoids deep imports to prevent
# circular dependencies and phantom module references.

from .signals import (
    OtherPowers_GovernanceSignal,
    OtherPowers_GovernanceSignalConsumer,
    OtherPowers_PostureAccumulator,
    OtherPowers_PostureSnapshot,
    Posture,
    SignalKind,
    IntelligenceMode,
    ExpressionEnvironment,
    DataCondition,
    Trend,
    Uncertainty,
    EvidenceClass,
    WithholdReason,
)

__all__ = [
    "OtherPowers_GovernanceSignal",
    "OtherPowers_GovernanceSignalConsumer",
    "OtherPowers_PostureAccumulator",
    "OtherPowers_PostureSnapshot",
    "Posture",
    "SignalKind",
    "IntelligenceMode",
    "ExpressionEnvironment",
    "DataCondition",
    "Trend",
    "Uncertainty",
    "EvidenceClass",
    "WithholdReason",
]


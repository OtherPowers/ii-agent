from enum import Enum
from typing import Optional, TypedDict


class SignalKind(str, Enum):
    GOVERNANCE = "governance"


class Posture(str, Enum):
    NEUTRAL = "neutral"
    INCREASE_CARE = "increase_care"
    HIGH_CARE = "high_care"


class Trend(str, Enum):
    FLAT = "flat"


class Uncertainty(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"


class EvidenceClass(str, Enum):
    WEAK = "weak"


class WithholdReason(str, Enum):
    INSUFFICIENT_SIGNAL = "insufficient_signal"
    UNCERTAINTY = "uncertainty"


class DataCondition(str, Enum):
    PARTIAL = "partial"


class IntelligenceMode(str, Enum):
    OBSERVATIONAL = "observational"
    LEARNING = "learning"


class OtherPowers_GovernanceSignalRecord(TypedDict, total=False):
    kind: SignalKind
    posture: Posture
    trend: Trend
    uncertainty: Uncertainty
    evidence: EvidenceClass
    withhold_reason: WithholdReason
    data_condition: DataCondition
    intelligence_mode: IntelligenceMode
    signal_strength: float


def new_signal(
    *,
    kind: SignalKind = SignalKind.GOVERNANCE,
    posture: Optional[Posture] = None,
    trend: Trend = Trend.FLAT,
    uncertainty: Uncertainty = Uncertainty.MODERATE,
    evidence: EvidenceClass = EvidenceClass.WEAK,
    withhold_reason: Optional[WithholdReason] = None,
    data_condition: DataCondition = DataCondition.PARTIAL,
    intelligence_mode: IntelligenceMode = IntelligenceMode.OBSERVATIONAL,
    signal_strength: float = 1.0,
) -> OtherPowers_GovernanceSignalRecord:
    return {
        "kind": kind,
        "posture": posture,
        "trend": trend,
        "uncertainty": uncertainty,
        "evidence": evidence,
        "withhold_reason": withhold_reason,
        "data_condition": data_condition,
        "intelligence_mode": intelligence_mode,
        "signal_strength": float(signal_strength),
    }


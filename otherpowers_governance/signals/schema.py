from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


class Posture(str, Enum):
    OPEN = "open"
    CAUTIOUS = "cautious"
    CLOSED = "closed"
    SILENT = "silent"


class Uncertainty(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    UNKNOWN = "unknown"


class IntelligenceMode(str, Enum):
    RECEPTIVE = "receptive"
    REFLECTIVE = "reflective"
    EXPRESSIVE = "expressive"
    WITHDRAWN = "withdrawn"


class WithholdReason(str, Enum):
    """
    Qualitative reason an emission was withheld.

    Non-evaluative.
    Non-ranking.
    Non-optimizable.
    """

    GOVERNANCE_BLOCK = "governance_block"
    CONSENT_WITHDRAWN = "consent_withdrawn"
    INSUFFICIENT_CONTEXT = "insufficient_context"
    SAFETY_REFUSAL = "safety_refusal"
    SELF_SILENCE = "self_silence"


@dataclass(frozen=True)
class GovernanceDecision:
    allow: bool
    reason: Optional[str] = None


@dataclass(frozen=True)
class SignalEnvelope:
    payload: Dict[str, Any]
    posture: Optional[Posture] = None
    uncertainty: Optional[Uncertainty] = None
    mode: Optional[IntelligenceMode] = None
    withhold_reason: Optional[WithholdReason] = None


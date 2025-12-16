from typing import Mapping

from otherpowers_governance.signals.schema import (
    Posture,
    Uncertainty,
    IntelligenceMode,
    WithholdReason,
)
from otherpowers_governance.signals.otherpowers_governance_signal import new_signal


class ColdStoragePostureEmissionBridge:
    """
    Translates long-horizon summaries into governance signals.
    Silence (None) is a first-class outcome.
    """

    def emit(self, summary: Mapping[str, object]):
        patterns = summary.get("pattern_families")
        if not patterns:
            return None

        pset = set(str(p) for p in patterns)

        # ------------------------------
        # VOLATILITY → SILENCE
        # ------------------------------
        if "volatility" in pset:
            return None

        if "care" in pset:
            return new_signal(
                posture=Posture.INCREASE_CARE,
                uncertainty=Uncertainty.HIGH,
                intelligence_mode=IntelligenceMode.LEARNING,
            )

        if "pressure" in pset or "capture" in pset:
            return new_signal(
                posture=Posture.HIGH_CARE,
                uncertainty=Uncertainty.HIGH,
                intelligence_mode=IntelligenceMode.OBSERVATIONAL,
            )

        # default: insufficient signal → silence
        return None


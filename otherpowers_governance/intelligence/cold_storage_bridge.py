from typing import Mapping

from otherpowers_governance.signals.schema import (
    Posture,
    Uncertainty,
    IntelligenceMode,
    WithholdReason,
)

# IMPORTANT:
# new_signal is sourced from the canonical signals API,
# not from a legacy or phantom module.
from otherpowers_governance.signals.api import new_signal


class ColdStoragePostureEmissionBridge:
    """
    Translates posture summaries into governance-safe emission records.

    This bridge may return None to indicate:
    - silence
    - governance refusal
    - intentional non-emission
    """

    def emit(self, summary: Mapping) -> Mapping | None:
        if not summary:
            return None

        posture = summary.get("posture")
        if posture is None:
            return None

        return new_signal(
            posture=Posture(posture),
            uncertainty=Uncertainty.UNKNOWN,
            mode=IntelligenceMode.REFLECTIVE,
            withhold=WithholdReason.NONE,
        )


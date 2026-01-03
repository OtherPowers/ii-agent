from typing import Mapping, Dict
import time

from otherpowers_governance.signals.schema import Posture


class FieldBalancer:
    """
    Balances governance signals across multiple axes, then resolves
    into a single posture.

    Axes (internal only):
    - care
    - volatility
    - erasure

    External interface remains unchanged.
    """

    def __init__(self):
        self._last_posture: Posture | None = None
        self._last_update: float | None = None

    def _extract_axes(self, signal: Mapping[str, object]) -> Dict[str, float]:
        """
        Pulls soft axis weights from signal metadata.
        Missing axes default to 0.0.
        """
        meta = signal.get("axes") or {}
        return {
            "care": float(meta.get("care", 0.0)),
            "volatility": float(meta.get("volatility", 0.0)),
            "erasure": float(meta.get("erasure", 0.0)),
        }

    def _resolve_posture(self, axes: Dict[str, float]) -> Posture:
        """
        Resolves axes into posture using conservative, abolitionist bias.
        """
        care = axes["care"]
        volatility = axes["volatility"]
        erasure = axes["erasure"]

        # Priority: erasure > volatility > care
        if erasure >= 0.7:
            return Posture.HIGH_CARE

        if volatility >= 0.7:
            return Posture.INCREASE_CARE

        if care >= 0.7:
            return Posture.INCREASE_CARE

        return Posture.NEUTRAL

    def balance(self, signal: Mapping[str, object]) -> Mapping[str, str]:
        axes = self._extract_axes(signal)
        posture = self._resolve_posture(axes)

        now = time.time()

        # Hysteresis: prevent rapid downshifts
        if self._last_posture is not None:
            if posture.value < self._last_posture.value:
                elapsed = now - (self._last_update or now)
                if elapsed < 30:
                    posture = self._last_posture

        self._last_posture = posture
        self._last_update = now

        return {
            "posture": posture.value,
            "confidence": signal.get("confidence", "moderate"),
            "reason": "aggregated",
        }


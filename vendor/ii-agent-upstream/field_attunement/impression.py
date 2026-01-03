from typing import Mapping, Dict, Optional
import time


class FieldImpression:
    """
    Forms an impression from field fragments without enforcing action.

    Axes are soft signals, not controls.
    Nothing here commands behavior.
    """

    def __init__(self):
        self._last_impression: Dict[str, object] | None = None
        self._last_update: float | None = None

    def _extract_axes(self, field: Mapping[str, object]) -> Dict[str, float]:
        meta = field.get("axes") or {}
        return {
            "care": float(meta.get("care", 0.0)),
            "volatility": float(meta.get("volatility", 0.0)),
            "erasure": float(meta.get("erasure", 0.0)),
        }

    def _form_impression(self, axes: Dict[str, float]) -> Dict[str, object]:
        care = axes["care"]
        volatility = axes["volatility"]
        erasure = axes["erasure"]

        if erasure >= 0.7:
            return {"posture": "care", "note": "protective presence"}

        if volatility >= 0.7:
            return {"posture": "care", "note": "stabilizing presence"}

        if care >= 0.7:
            return {"posture": "open", "note": "supportive presence"}

        return {"posture": "open", "note": "ambient"}

    def impression(self, field: Mapping[str, object]) -> Mapping[str, object]:
        axes = self._extract_axes(field)
        impression = self._form_impression(axes)

        now = time.time()

        # Soft hysteresis: avoid rapid tonal shifts
        if self._last_impression is not None:
            elapsed = now - (self._last_update or now)
            if elapsed < 30:
                impression = self._last_impression

        self._last_impression = impression
        self._last_update = now

        return impression


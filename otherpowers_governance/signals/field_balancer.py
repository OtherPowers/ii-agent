from typing import Mapping, Dict, Any, Optional
import time

from field_attunement.field import read_field
from field_attunement.impression import FieldImpression


class FieldBalancer:
    """
    Softly resolves signal axes into a field-level posture impression.

    - No consumers
    - No enforcement
    - No ranking
    - Memory exists only to prevent tonal whiplash
    """

    def __init__(self):
        self._last_posture: Optional[str] = None
        self._last_update: Optional[float] = None
        self._impression = FieldImpression()

    def _extract_axes(self, signal: Mapping[str, Any]) -> Dict[str, float]:
        axes = signal.get("axes") or {}
        return {
            "care": float(axes.get("care", 0.0)),
            "volatility": float(axes.get("volatility", 0.0)),
            "erasure": float(axes.get("erasure", 0.0)),
        }

    def balance(self, signal: Mapping[str, Any]) -> Dict[str, Any]:
        field = read_field()
        axes = self._extract_axes(signal)

        layered_field = {
            **field,
            "axes": axes,
        }

        impression = self._impression.impression(layered_field)
        posture = impression.get("posture")

        now = time.time()

        if self._last_posture is not None and posture != self._last_posture:
            elapsed = now - (self._last_update or now)
            if elapsed < 30:
                posture = self._last_posture

        self._last_posture = posture
        self._last_update = now

        return {
            "posture": posture,
            "confidence": signal.get("confidence", "medium"),
            "reason": impression.get("note", "field-impression"),
        }


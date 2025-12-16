from dataclasses import dataclass
from typing import Dict, Any, Optional
import math
import time


@dataclass
class FieldModulation:
    tempo: float
    curiosity: float
    optimization_pressure: float
    expressive_range: float
    silence_affinity: float
    perspective_rotation: float


class FieldAttuner:
    """
    Read-only, non-surveillant.
    Senses the field and gently attunes internal behavior.

    No memory.
    No enforcement.
    No observation of entities.
    """

    def __init__(self):
        self._last_seen: Optional[float] = None

    def attune(self, field_state: Optional[Dict[str, Any]]) -> FieldModulation:
        now = time.time()

        if not field_state:
            return self._neutral()

        posture = field_state.get("posture", "neutral")
        confidence = field_state.get("confidence", "low")

        weight = self._confidence_weight(confidence)
        decay = self._decay(now)

        if posture == "silence":
            return self._silence(weight, decay)

        if posture == "increase_care":
            return self._care(weight, decay)

        if posture == "high_care":
            return self._high_care(weight, decay)

        return self._neutral()

    # profiles

    def _neutral(self) -> FieldModulation:
        return FieldModulation(
            tempo=1.0,
            curiosity=1.0,
            optimization_pressure=1.0,
            expressive_range=1.0,
            silence_affinity=0.2,
            perspective_rotation=0.2,
        )

    def _silence(self, w: float, d: float) -> FieldModulation:
        amp = w * d
        return FieldModulation(
            tempo=1.0 - 0.4 * amp,
            curiosity=0.9,
            optimization_pressure=0.4,
            expressive_range=0.6 + 0.2 * amp,
            silence_affinity=min(1.0, 0.6 + 0.4 * amp),
            perspective_rotation=0.8 * amp,
        )

    def _care(self, w: float, d: float) -> FieldModulation:
        amp = w * d
        return FieldModulation(
            tempo=1.0 - 0.2 * amp,
            curiosity=1.0 + 0.3 * amp,
            optimization_pressure=0.7,
            expressive_range=1.2,
            silence_affinity=0.4,
            perspective_rotation=0.5 * amp,
        )

    def _high_care(self, w: float, d: float) -> FieldModulation:
        amp = w * d
        return FieldModulation(
            tempo=1.0 - 0.5 * amp,
            curiosity=1.2,
            optimization_pressure=0.4,
            expressive_range=1.4,
            silence_affinity=0.6,
            perspective_rotation=0.7 * amp,
        )

    def _confidence_weight(self, confidence: str) -> float:
        return {
            "low": 0.3,
            "moderate": 0.6,
            "high": 1.0,
        }.get(confidence, 0.3)

    def _decay(self, now: float) -> float:
        if self._last_seen is None:
            self._last_seen = now
            return 1.0

        dt = now - self._last_seen
        self._last_seen = now
        return math.exp(-dt / 60.0)


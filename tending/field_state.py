from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass(frozen=True)
class TemporalDecayCloud:
    """
    Residual harm or pressure that thins expressive capacity over time.
    Decays naturally. Cannot be cleared by compliance or intent.
    """

    magnitude: float          # 0.0 – 1.0
    half_life_hours: float
    created_utc: datetime

    def remaining(self, now: datetime) -> float:
        elapsed_hours = (now - self.created_utc).total_seconds() / 3600
        if elapsed_hours <= 0:
            return self.magnitude

        decay_factor = 0.5 ** (elapsed_hours / self.half_life_hours)
        return max(0.0, self.magnitude * decay_factor)


@dataclass(frozen=True)
class FieldState:
    """
    Atmospheric snapshot of the creative intelligence field.

    No identity.
    No memory.
    No attribution.
    """

    timestamp_utc: datetime
    seasons: List[str]
    diurnal_phase: str

    decay_clouds: List[TemporalDecayCloud] = field(default_factory=list)
    baseline_density: float = 1.0

    @property
    def expressive_density(self) -> float:
        """
        Remaining expressive capacity after temporal decay is applied.
        """

        residue = sum(
            cloud.remaining(self.timestamp_utc)
            for cloud in self.decay_clouds
        )

        density = self.baseline_density - residue
        return max(0.0, min(1.0, density))


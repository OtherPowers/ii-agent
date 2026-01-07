from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List
import os


@dataclass(frozen=True)
class FieldState:
    """
    Snapshot of the field.

    This object is descriptive only.
    It never evaluates, scores, or predicts.
    """

    timestamp_utc: datetime
    seasons: List[str]
    diurnal_phase: str
    expressive_density: float = 1.0

    @classmethod
    def now(cls) -> "FieldState":
        """
        Canonical field constructor.

        Deterministic, timezone-safe, test-safe.
        """
        fixed = os.environ.get("OTHERPOWERS_FIXED_TIME")
        if fixed:
            ts = datetime.fromisoformat(fixed)
        else:
            ts = datetime.now(timezone.utc)

        # Canonical minimal defaults
        return cls(
            timestamp_utc=ts,
            seasons=["winter"],
            diurnal_phase="day",
            expressive_density=1.0,
        )


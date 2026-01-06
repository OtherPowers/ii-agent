from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass(frozen=True)
class FieldState:
    """
    Internal, non-public field representation.

    This model may grow without changing the emission surface.
    """
    timestamp_utc: datetime
    seasons: List[str]
    diurnal_phase: str


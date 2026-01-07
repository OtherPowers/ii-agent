from dataclasses import dataclass
from datetime import datetime
from typing import List, Literal


Season = Literal["spring", "summer", "autumn", "winter"]
DiurnalPhase = Literal["dawn", "day", "dusk", "night"]


@dataclass(frozen=True)
class FieldState:
    """
    Internal representation of the Creative Intelligence Field state.

    This model is:
    - non-public
    - deterministic
    - identity-free
    - safe to construct in isolation

    It must remain importable without side effects.
    """

    timestamp_utc: datetime
    seasons: List[Season]
    diurnal_phase: DiurnalPhase


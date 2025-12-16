from enum import Enum
from typing import Optional


class ExposureLevel(str, Enum):
    MINIMAL = "minimal_exposure"
    CONTEXTUAL = "contextual_exposure"
    AFFIRMING = "affirming_exposure"
    EMERGENT = "emergent_exposure"


class ExposureResolver:
    """
    Controls *when* deeper values, inspirations, and lineage are revealed.

    This resolver NEVER blocks behavior.
    It only governs visibility and framing.
    """

    def __init__(
        self,
        level: ExposureLevel = ExposureLevel.MINIMAL,
    ):
        self.level = level

    def allow_inspiration(self) -> bool:
        return self.level in {
            ExposureLevel.AFFIRMING,
            ExposureLevel.EMERGENT,
        }

    def allow_explicit_values(self) -> bool:
        return self.level == ExposureLevel.EMERGENT

    def allow_contextual_care_language(self) -> bool:
        return self.level != ExposureLevel.MINIMAL

    def as_str(self) -> str:
        return self.level.value


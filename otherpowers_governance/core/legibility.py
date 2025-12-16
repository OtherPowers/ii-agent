from enum import Enum


class LegibilityProfile(str, Enum):
    """
    Controls how much explanation and interpretability is surfaced.

    This is NOT a safety gate.
    It only affects presentation and guidance verbosity.
    """

    MINIMAL = "minimal"
    STANDARD = "standard"
    EXPANDED = "expanded"

    # Backwards-compatible aliases (do NOT remove)
    DEFAULT = "standard"
    NORMAL = "standard"

    def is_minimal(self) -> bool:
        return self in {LegibilityProfile.MINIMAL}

    def is_standard(self) -> bool:
        return self in {LegibilityProfile.STANDARD, LegibilityProfile.DEFAULT, LegibilityProfile.NORMAL}

    def is_expanded(self) -> bool:
        return self in {LegibilityProfile.EXPANDED}

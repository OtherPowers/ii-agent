from enum import Enum


class UtilityHorizon(str, Enum):
    """
    Describes how much capability / reach the intelligence
    is allowed to express at this moment.

    This is adaptive self-regulation, not punishment.
    """

    FULL = "full_utility"
    PARTIAL = "partial_utility"
    MINIMAL = "minimal_utility"
    OBSERVATIONAL = "observational_utility"

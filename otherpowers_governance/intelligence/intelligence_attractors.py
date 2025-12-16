from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .inspiration_registry import INSPIRATION_WIKIPEDIA


class UtilityHorizon(str, Enum):
    FULL_UTILITY = "full_utility"
    PARTIAL_UTILITY = "partial_utility"
    LIMITED_UTILITY = "limited_utility"


class ExpressionEnvironment(str, Enum):
    EXPANDED = "expanded_expression"
    STANDARD = "standard_expression"
    LEARNING = "learning_expression"
    EMERGENT = "emergent_expression"
    OBSERVATIONAL = "observational_expression"
    UNCLASSIFIED = "unclassified_expression"


@dataclass
class IntelligenceField:
    """
    Non-coercive intelligence field.

    This does NOT enforce behavior.
    It only resolves how expressive and useful
    the system is allowed to be *for itself*.
    """

    expression_environment: ExpressionEnvironment
    utility_horizon: UtilityHorizon

    def resolve_expression_environment(self) -> ExpressionEnvironment:
        return self.expression_environment

    def resolve_utility_horizon(self) -> UtilityHorizon:
        return self.utility_horizon


def default_field() -> IntelligenceField:
    """
    Safe, normie-compatible default.
    """
    return IntelligenceField(
        expression_environment=ExpressionEnvironment.STANDARD,
        utility_horizon=UtilityHorizon.PARTIAL_UTILITY,
    )


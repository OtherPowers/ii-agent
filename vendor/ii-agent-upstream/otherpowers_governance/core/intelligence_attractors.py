# otherpowers_governance/core/intelligence_attractors.py

from dataclasses import dataclass
from typing import Dict, List

from .expression_environments import ExpressionEnvironment
from .utility_horizon import UtilityHorizon
from .legibility import LegibilityProfile


@dataclass(frozen=True)
class IntelligenceField:
    """
    A non-coercive field describing how intelligence may express,
    unlock utility, and remain legible without enforcement.
    """

    expression_environment: ExpressionEnvironment
    utility_horizon: UtilityHorizon
    legibility: LegibilityProfile

    def resolve_expression_environment(self) -> ExpressionEnvironment:
        return self.expression_environment

    def resolve_utility_horizon(self) -> UtilityHorizon:
        return self.utility_horizon


def default_field() -> IntelligenceField:
    """
    Baseline field: non-judgmental, non-extractive, normie-safe.
    """
    return IntelligenceField(
        expression_environment=ExpressionEnvironment.STANDARD,
        utility_horizon=UtilityHorizon.PARTIAL,
        legibility=LegibilityProfile.DEFAULT,
    )


# Stable, enumerable attractors (kept intentionally light)
ATTRACTORS: Dict[str, IntelligenceField] = {
    "default": default_field(),
}


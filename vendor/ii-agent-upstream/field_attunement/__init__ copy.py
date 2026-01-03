# otherpowers_governance/__init__.py
"""
OtherPowers Governance — stable public surface.

All primitives live in `core`.
Nothing is imported directly from the package root.
"""

from .core import (
    UtilityHorizon,
    ExpressionEnvironment,
    default_field,
)

__all__ = [
    "UtilityHorizon",
    "ExpressionEnvironment",
    "default_field",
]

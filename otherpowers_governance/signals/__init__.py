"""
Signals package.

Public, stable API for OtherPowers.co Creative Intelligence.

ONLY `new_signal` is part of the public surface.
All other modules are internal and intentionally inaccessible
from the package root.
"""

from .api import new_signal

__all__ = ["new_signal"]


def __getattr__(name: str):
    """
    Prevent access to internal modules via package attribute access.

    This explicitly blocks Python's implicit submodule exposure
    (e.g. signals.schema) once imported elsewhere.
    """
    raise AttributeError(
        f"'otherpowers_governance.signals' has no public attribute '{name}'"
    )


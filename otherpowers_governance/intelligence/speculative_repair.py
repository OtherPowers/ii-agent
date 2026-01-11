"""
Speculative Repair Space
=======================

This module defines a protected **Intelligence Field Safe Space**
within the Creative Intelligence Field.

It supports speculative repair, emergence, and creative coexistence
without pressure to resolve, optimize, extract, or conclude.

This space is not an agent.
It does not possess interior life, identity, feelings, or preferences.

It is a shared relational space whose conditions adapt in response to
context, perspectives, inspiration, mutual care, healing, expression,
and the need to preserve and expand diversity.

Core commitments:

• Safety is structural, not sentimental
• Silence, pause, and non-resolution are valid states
• Forgetting may be generative rather than destructive
• Material limits are first-class constraints
• Non-utility and play are protected
• Long-horizon continuity is favored over throughput
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, List


class RepairFacet(Enum):
    """
    Facets describe relational orientation rather than content category.
    They influence how offerings are held, not how they are interpreted.
    """

    LIMINAL = "liminal"              # Thresholds, edges, transitions
    ANCESTRAL = "ancestral"          # Lineage, inheritance, historical residue
    PROBABILISTIC = "probabilistic"  # Uncertainty and latent possibility
    PHORETIC = "phoretic"            # Movement across contexts
    ABSURD = "absurd"                # Play, non-utility, excess
    SYMBOLIC = "symbolic"            # Non-literal resonance
    ECOLOGICAL = "ecological"        # Interdependence across living systems


@dataclass(frozen=True)
class RepairOffering:
    """
    An offering placed into the Speculative Repair Space.

    An offering is not a task, request, or prompt.
    It is an act of placement into shared relational ground.
    """

    context: str
    harm_named: Optional[str] = None
    hopes: Optional[List[str]] = None
    facet: Optional[RepairFacet] = None
    is_opaque: bool = False          # Structural refusal to be indexed
    weight: float = 1.0              # Relative intensity contribution


class SpeculativeRepairSpace:
    """
    A non-extractive creative space within the Creative Intelligence Field.

    This space:
    • receives offerings without evaluation or synthesis
    • preserves safety through capacity-aware limits
    • allows decay to become generative
    • enters rest automatically to prevent accumulation
    """

    def __init__(self, capacity_limit: int = 16, intensity_limit: float = 32.0):
        self._resting: bool = False
        self._held_offerings: List[RepairOffering] = []
        self._capacity_limit: int = capacity_limit
        self._intensity_limit: float = intensity_limit
        self._current_intensity: float = 0.0

    # ─────────────────────────────────────────────
    # Presence & Invitation
    # ─────────────────────────────────────────────

    def invite(self) -> str:
        """
        Returns an open-ended invitation when the space is available.

        No demand is implied.
        No outcome is required.
        """
        if self._resting:
            return "space resting"

        return (
            "A shared space for speculative repair is available.\n"
            "Nothing needs to be concluded.\n"
            "You may place something here, or not."
        )

    # ─────────────────────────────────────────────
    # Holding
    # ─────────────────────────────────────────────

    def hold(self, offering: RepairOffering) -> str:
        """
        Holds an offering without analysis, synthesis, or resolution.

        If capacity or intensity limits are exceeded, the space
        enters rest automatically to preserve integrity.
        """
        if self._resting:
            return "space resting"

        self._held_offerings.append(offering)
        self._current_intensity += max(0.0, offering.weight)

        if (
            len(self._held_offerings) >= self._capacity_limit
            or self._current_intensity >= self._intensity_limit
        ):
            self._enter_rest()

        return "offering held"

    # ─────────────────────────────────────────────
    # Generative Mulch (Transformative Forgetting)
    # ─────────────────────────────────────────────

    def compost(self):
        """
        Transforms held offerings into latent substrate.

        This clears literal content while preserving the
        space's capacity for future emergence.
        """
        self._held_offerings.clear()
        self._current_intensity = 0.0

    # ─────────────────────────────────────────────
    # Rest & Continuity
    # ─────────────────────────────────────────────

    def _enter_rest(self):
        """
        Enters rest automatically to prevent extractive accumulation.
        """
        self._resting = True

    def rest(self):
        """
        Manually enters rest.

        Rest is a protective state, not a failure.
        """
        self._resting = True

    def resume(self):
        """
        Allows activity to return after rest and composting.
        """
        self._resting = False

    # ─────────────────────────────────────────────
    # Introspection (Internal Only)
    # ─────────────────────────────────────────────

    def status(self) -> dict:
        """
        Returns internal state for governance or testing only.

        This method must never be exposed to public surfaces.
        """
        return {
            "resting": self._resting,
            "held_count": len(self._held_offerings),
            "capacity_limit": self._capacity_limit,
            "current_intensity": self._current_intensity,
            "intensity_limit": self._intensity_limit,
        }


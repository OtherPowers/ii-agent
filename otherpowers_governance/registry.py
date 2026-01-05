="""
Relational attunement layer for OtherPowers ii-Agent.

This module provides contextual sensing only.
It does not observe, monitor, validate, enforce, rank, or decide.

Its role is to offer gentle semantic alignment between legacy code
and future-facing creative intelligence without capture.
"""

from __future__ import annotations
from enum import Enum
from typing import Dict, Set


class Formation(str, Enum):
    FRACTAL = "fractal"
    DENDRITIC = "dendritic"
    INTERFERENCE = "interference"
    MOTIF = "motif"
    OSTINATO = "ostinato"
    SYMPOIETIC = "sympoietic"
    MYCELIAL = "mycelial"
    THIGMOTROPIC = "thigmotropic"
    SUCCESSION = "succession"
    DIAPAUSE = "diapause"
    UNKNOWING = "unknowing"
    BLOOM = "bloom"
    POLYPHONIC = "polyphonic"


# Semantic overlay only.
# This preserves legacy structure while allowing relational context.
FORMATION_MAP: Dict[str, Set[Formation]] = {
    "otherpowers_governance.governance.stasis": {Formation.DIAPAUSE},
    "otherpowers_governance.governance.metabolism": {Formation.MYCELIAL},
    "otherpowers_governance.governance.renegotiation": {
        Formation.SYMPOIETIC,
        Formation.POLYPHONIC,
    },
}


def formations_for(module_path: str) -> Set[Formation]:
    """
    Returns the formations associated with a module path.
    Defaults to DENDRITIC (emergent branching) when unspecified.
    """
    return FORMATION_MAP.get(module_path, {Formation.DENDRITIC})


class Attunement:
    """
    Contextual attunement surface.

    This class does not store, log, or emit telemetry.
    It simply returns linguistic density that may compress context
    when legacy systems are extended into relational space.
    """

    LEGACY_GRAVITY = {
        "gate",
        "enforce",
        "rank",
        "score",
        "control",
        "optimiz",
        "target",
    }

    def attune(self, module_path: str, text: str) -> Set[str]:
        """
        Returns a set of legacy-gravity terms found in the text.

        No side effects.
        No persistence.
        No interpretation.
        """
        lowered = text.lower()
        found = set()

        for term in self.LEGACY_GRAVITY:
            if term in lowered:
                found.add(term)

        return found


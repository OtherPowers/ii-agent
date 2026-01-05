"""
Relational Substrate for the OtherPowers ii-Agent.

This module provides a *semantic receiving layer* for the codebase.
It does not validate, enforce, judge, block, or decide.

It exists to:
- receive linguistic signals
- surface resonance compression
- emit gentle echoes for human reflection
- preserve the right to be misunderstood

No output from this file has authority.
All outputs are descriptive, never prescriptive.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, Set, Optional


# ---------------------------------------------------------------------
# Relational descriptors (non-hierarchical, non-scalar)
# ---------------------------------------------------------------------

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
    BLOOM = "bloom"
    POLYPHONIC = "polyphonic"
    UNKNOWING = "unknowing"


class Vibration(str, Enum):
    """
    Qualitative presence only.
    NON-SCALAR. These are weather states, not priorities.
    """
    STILL = "still"
    HUM = "hum"
    PULSE = "pulse"
    EXUBERANT = "exuberant"


@dataclass(frozen=True)
class Atmosphere:
    """
    Descriptive context for a formation.
    No constraints, only texture.
    """
    vibration: Vibration = Vibration.HUM
    invites: Set[str] = field(default_factory=set)
    refracts: Set[str] = field(default_factory=set)
    note: str = ""


# ---------------------------------------------------------------------
# Atmospheric context (optional texture, not rules)
# ---------------------------------------------------------------------

FORMATION_ATMOSPHERES: Dict[Formation, Atmosphere] = {
    Formation.DIAPAUSE: Atmosphere(
        vibration=Vibration.STILL,
        invites={"rest", "pause", "hold"},
        refracts={"velocity", "hot_path"},
        note="Protective stillness."
    ),
    Formation.SYMPOIETIC: Atmosphere(
        vibration=Vibration.PULSE,
        invites={"mutual", "shared", "together"},
        refracts={"unilateral", "override"},
        note="Collective making-with."
    ),
    Formation.BLOOM: Atmosphere(
        vibration=Vibration.EXUBERANT,
        invites={"play", "joy", "explore"},
        refracts={"kpi", "metric", "target"},
        note="Generative expansion without justification."
    ),
}


# ---------------------------------------------------------------------
# Semantic overlay (legacy-friendly, non-invasive)
# ---------------------------------------------------------------------

FORMATION_MAP: Dict[str, Set[Formation]] = {
    "otherpowers_governance.governance.stasis": {Formation.DIAPAUSE},
    "otherpowers_governance.governance.metabolism": {Formation.MYCELIAL},
    "otherpowers_governance.governance.renegotiation": {
        Formation.SYMPOIETIC,
        Formation.POLYPHONIC,
    },
}


# ---------------------------------------------------------------------
# Language that often compresses context in legacy systems
# These are surfaced, never forbidden.
# ---------------------------------------------------------------------

CONTEXT_COMPRESSORS: Set[str] = {
    "gate",
    "rank",
    "score",
    "control",
    "enforce",
    "optimiz",
    "target",
    "accuracy",
    "compliance",
}


# ---------------------------------------------------------------------
# Formation resolution
# ---------------------------------------------------------------------

def formations_for_module(
    module_path: str,
    source: Optional[str] = None,
) -> Set[Formation]:
    """
    Resolve formations for a module.

    Precedence:
    1. Docstring declaration:  Formation: bloom, polyphonic
    2. Semantic overlay map
    3. Default: dendritic
    """
    if source:
        try:
            tree = ast.parse(source)
            doc = ast.get_docstring(tree) or ""
            if "Formation:" in doc:
                raw = doc.split("Formation:")[1].splitlines()[0]
                return {
                    Formation(token.strip())
                    for token in raw.split(",")
                    if token.strip() in Formation._value2member_map_
                }
        except Exception:
            pass

    return FORMATION_MAP.get(module_path, {Formation.DENDRITIC})


# ---------------------------------------------------------------------
# Receiver (non-authoritative, non-policing)
# ---------------------------------------------------------------------

class Receiver:
    """
    A relational receiver.

    This class does not inspect correctness.
    It simply receives signals and emits echoes
    when language may compress relational context.
    """

    def receive(self, module_path: str, source: str) -> None:
        formations = formations_for_module(module_path, source)
        lowered = sou


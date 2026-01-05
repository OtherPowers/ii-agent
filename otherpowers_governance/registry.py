"""
Relational Substrate for the OtherPowers ii-Agent.

This module provides a non-authoritative receiver layer.
It reflects language and structure without enforcing outcomes.

Nothing here blocks execution.
Nothing here decides correctness.
Everything here is descriptive and optional.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, Set, Optional


# -----------------------------
# Relational descriptors
# -----------------------------

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
    STILL = "still"
    HUM = "hum"
    PULSE = "pulse"
    EXUBERANT = "exuberant"


@dataclass(frozen=True)
class Atmosphere:
    vibration: Vibration = Vibration.HUM
    invites: Set[str] = field(default_factory=set)
    refracts: Set[str] = field(default_factory=set)
    note: str = ""


# -----------------------------
# Soft maps (descriptive only)
# -----------------------------

FORMATION_MAP: Dict[str, Set[Formation]] = {
    "otherpowers_governance.governance.stasis": {Formation.DIAPAUSE},
    "otherpowers_governance.governance.metabolism": {Formation.MYCELIAL},
    "otherpowers_governance.governance.renegotiation": {
        Formation.SYMPOIETIC,
        Formation.POLYPHONIC,
    },
}

# Language that compresses context or flattens relational meaning.
# NOTE: Explicitly excludes legacy control/optimization metaphors.
COMPRESSIVE_TERMS: Set[str] = {
    "rank",
    "score",
    "control",
    "enforce",
    "target",
    "accuracy",
    "compliance",
}


# -----------------------------
# Formation resolution
# -----------------------------

def formations_for_module(module_path: str, source: Optional[str] = None) -> Set[Formation]:
    if source:
        try:
            tree = ast.parse(source)
            doc = ast.get_docstring(tree) or ""
            if "Formation:" in doc:
                raw = doc.split("Formation:")[1].splitlines()[0]
                return {
                    Formation(v.strip())
                    for v in raw.split(",")
                    if v.strip() in Formation._value2member_map_
                }
        except Exception:
            pass

    return FORMATION_MAP.get(module_path, {Formation.DENDRITIC})


# -----------------------------
# Receiver layer (non-authoritative)
# -----------------------------

class Receiver:
    """
    Receives and reflects linguistic density.
    Emits context notes only.
    """

    def receive(self, module_path: str, source: str) -> None:
        lowered = source.lower()
        formations = formations_for_module(module_path, source)

        for term in COMPRESSIVE_TERMS:
            if term in lowered:
                print(
                    f"[echo] {module_path} contains '{term}' "
                    f"(context may compress; posture={sorted(f.value for f in formations)})"
                )


# -----------------------------
# Public entry point
# -----------------------------

def receive_tree(root: str = "otherpowers_governance") -> None:
    """
    Walks the repository and receives current resonance.
    Never raises.
    Never exits.
    """
    receiver = Receiver()

    for path in Path(root).rglob("*.py"):
        try:
            receiver.receive(
                str(path),
                path.read_text(encoding="utf-8")
            )
        except Exception as e:
            print(f"[residue] unable to read {path}: {e}")


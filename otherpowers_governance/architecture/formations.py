"""
Formation overlay for OtherPowers ii-Agent.

This module is an intentionally minimal semantic registry that maps the expanded
OtherPowers formations into a stable, importable contract.

Design constraints:
- No dependency on runtime state.
- No side effects.
- No new folder taxonomies.
- Legacy legible naming that still carries abolitionist intent.

Abolitionist posture in code form:
- We treat fragmentation as valid structure, not a defect.
- We treat silence as a first-class outcome, not an error.
- We treat non-extractive behavior as an invariant, not a preference.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Iterable, Optional


class FormationId(str, Enum):
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


@dataclass(frozen=True)
class Formation:
    """
    A Formation is a named relational shape.

    It is not a feature and not a folder boundary.
    It is an interpretive layer that remains stable while implementation evolves.
    """

    id: FormationId
    legacy_alias: str
    one_line: str
    invariants: tuple[str, ...]


_REGISTRY: Dict[FormationId, Formation] = {
    FormationId.FRACTAL: Formation(
        id=FormationId.FRACTAL,
        legacy_alias="hierarchical-decomposition",
        one_line="Patterns repeat across scales without forcing sameness across contexts.",
        invariants=(
            "Supports multi-scale interpretation.",
            "Avoids single-summary collapse.",
        ),
    ),
    FormationId.DENDRITIC: Formation(
        id=FormationId.DENDRITIC,
        legacy_alias="branching-evidence-graph",
        one_line="Meaning grows via branching paths rather than a single chain of reasoning.",
        invariants=(
            "Allows multiple concurrent threads.",
            "Does not demand convergence.",
        ),
    ),
    FormationId.INTERFERENCE: Formation(
        id=FormationId.INTERFERENCE,
        legacy_alias="signal-superposition",
        one_line="Conflicting truths can coexist without averaging into a false compromise.",
        invariants=(
            "Rejects forced synthesis.",
            "Preserves minority and edge signals.",
        ),
    ),
    FormationId.MOTIF: Formation(
        id=FormationId.MOTIF,
        legacy_alias="recurrent-theme",
        one_line="Recurring motifs encode continuity without requiring identical repetition.",
        invariants=(
            "Tracks recurrence without overfitting.",
            "Allows drift while maintaining lineage.",
        ),
    ),
    FormationId.OSTINATO: Formation(
        id=FormationId.OSTINATO,
        legacy_alias="steady-background-process",
        one_line="Some care work is continuous and quiet, and still central to system health.",
        invariants=(
            "Honors ongoing maintenance work.",
            "Does not treat quiet as absence.",
        ),
    ),
    FormationId.SYMPOIETIC: Formation(
        id=FormationId.SYMPOIETIC,
        legacy_alias="co-creation",
        one_line="Outcomes are made together, without extraction or domination.",
        invariants=(
            "No coercive convergence.",
            "No value capture from vulnerable actors.",
        ),
    ),
    FormationId.MYCELIAL: Formation(
        id=FormationId.MYCELIAL,
        legacy_alias="distributed-knowledge-network",
        one_line="Knowledge travels through resilient, partial, low-visibility pathways.",
        invariants=(
            "Survives partial failure.",
            "Works without centralized authority.",
        ),
    ),
    FormationId.THIGMOTROPIC: Formation(
        id=FormationId.THIGMOTROPIC,
        legacy_alias="constraint-responsive-adaptation",
        one_line="The system adapts to contact with constraints without escalating harm.",
        invariants=(
            "Adapts without retaliation.",
            "Reduces harm under pressure.",
        ),
    ),
    FormationId.SUCCESSION: Formation(
        id=FormationId.SUCCESSION,
        legacy_alias="phase-shift",
        one_line="Systems evolve through phases without pretending the prior phase was wrong.",
        invariants=(
            "Explicitly supports phases.",
            "Avoids rewrite spirals.",
        ),
    ),
    FormationId.DIAPAUSE: Formation(
        id=FormationId.DIAPAUSE,
        legacy_alias="intentional-stasis",
        one_line="Strategic stillness prevents extractive urgency and protects safety.",
        invariants=(
            "Silence is valid output.",
            "No forced action for completeness.",
        ),
    ),
}


def get_formation(formation_id: FormationId) -> Formation:
    return _REGISTRY[formation_id]


def list_formations() -> Iterable[Formation]:
    return _REGISTRY.values()


def maybe_parse_formation_id(value: Optional[str]) -> Optional[FormationId]:
    if not value:
        return None
    value = value.strip().lower()
    for fid in FormationId:
        if fid.value == value:
            return fid
    return None


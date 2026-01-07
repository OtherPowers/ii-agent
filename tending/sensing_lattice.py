# tending/sensing_lattice.py

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Literal

from tending.field_state import FieldState


Posture = Literal[
    "open",
    "listening",
    "holding",
    "resting",
    "emergent",
    "sparse",
]


@dataclass(frozen=True)
class SensingLattice:
    """
    Deterministic atmospheric state.

    This structure NEVER alters:
    - stdout schema
    - exit codes
    - side effects

    It only shapes expressive texture downstream.
    """

    postures: List[Posture]
    resonance_notes: List[str]
    bloom_conditions: List[str]
    silence_is_protective: bool
    expressive_density: float


def attune(field: FieldState) -> SensingLattice:
    """
    ABI-safe attunement.

    Density modulates texture, not permission.
    """
    postures: List[Posture] = ["listening"]
    resonance_notes: List[str] = []
    bloom_conditions: List[str] = []

    density = field.expressive_density  # scalar, not callable

    protective = False

    # protective overlaps
    if "winter" in field.seasons:
        postures.append("holding")
        resonance_notes.append("depth over visibility")
        protective = True

    if field.diurnal_phase in ("night", "dawn"):
        postures.append("resting")
        resonance_notes.append("silence stabilizes")
        protective = True

    # expressive thinning
    if density < 0.4:
        postures.append("sparse")
        resonance_notes.append("signal thins to protect capacity")

    # bloom evaporates under protection or low density
    if not protective and density >= 0.7:
        if "spring" in field.seasons and field.diurnal_phase in ("day", "dusk"):
            postures.append("emergent")
            bloom_conditions.append("co-creation without urgency")

    # preserve order, remove duplicates
    postures = list(dict.fromkeys(postures))
    resonance_notes = list(dict.fromkeys(resonance_notes))
    bloom_conditions = list(dict.fromkeys(bloom_conditions))

    return SensingLattice(
        postures=postures,
        resonance_notes=resonance_notes,
        bloom_conditions=bloom_conditions,
        silence_is_protective=True,
        expressive_density=density,
    )


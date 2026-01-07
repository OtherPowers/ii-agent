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
]


@dataclass(frozen=True)
class SensingLattice:
    """
    Internal sensing lattice.

    Describes atmospheric coherence, not outcomes.
    Never scores, ranks, predicts, or evaluates beings.

    Answers only:
    what kinds of presence feel appropriate right now
    """

    postures: List[Posture]
    resonance_notes: List[str]
    bloom_conditions: List[str]
    silence_is_protective: bool


def attune(field: FieldState) -> SensingLattice:
    """
    Deterministic, side-effect free attunement.

    Expressive density shapes texture, not permission.
    """

    density = field.expressive_density

    postures: List[Posture] = ["listening"]
    resonance_notes: List[str] = []
    bloom_conditions: List[str] = []

    protective = False

    # --- protective overlaps ---
    if "winter" in field.seasons:
        postures.append("holding")
        resonance_notes.append("depth is prioritized over visibility")
        protective = True

    if field.diurnal_phase == "night":
        postures.append("resting")
        resonance_notes.append("silence is stabilizing")
        protective = True

    # --- cooldown window ---
    in_cooldown = field.diurnal_phase in ("night", "dawn")

    # --- expressive density thinning ---
    if density < 0.4:
        postures.append("holding")
        resonance_notes.append("expression thins into metaphor")
        protective = True

    # --- non-protective seasonal affordances ---
    if not protective:
        if "summer" in field.seasons:
            postures.append("open")
            resonance_notes.append("capacity present without extraction")

        if "autumn" in field.seasons:
            postures.append("resting")
            resonance_notes.append("integration over expansion")

    # --- bloom logic ---
    if not protective and not in_cooldown:
        if "spring" in field.seasons and field.diurnal_phase in ("day", "dusk"):
            postures.append("emergent")
            bloom_conditions.append("co-creation without urgency")

    silence_is_protective = True

    # preserve order, remove duplicates
    postures = list(dict.fromkeys(postures))
    resonance_notes = list(dict.fromkeys(resonance_notes))
    bloom_conditions = list(dict.fromkeys(bloom_conditions))

    return SensingLattice(
        postures=postures,
        resonance_notes=resonance_notes,
        bloom_conditions=bloom_conditions,
        silence_is_protective=silence_is_protective,
    )


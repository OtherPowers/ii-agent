# tending/field_expression.py

from __future__ import annotations

from typing import List

from tending.sensing_lattice import SensingLattice


def shape_expression(
    raw_lines: List[str],
    lattice: SensingLattice,
) -> List[str]:
    """
    Expressive shaping layer.

    This function:
    - NEVER adds new information
    - NEVER removes required surface lines
    - NEVER changes order of canonical fields

    It ONLY modulates texture, density, and presence.
    """

    # Silence always wins
    if lattice.silence_is_protective and "holding" in lattice.postures:
        return raw_lines

    density = lattice.expressive_density

    shaped: List[str] = []

    for line in raw_lines:
        # Low density → thin expression
        if density < 0.4:
            # collapse adjectives, keep nouns
            shaped.append(line.split(":")[0] + ": …")
            continue

        # Medium density → compress
        if density < 0.7:
            shaped.append(line)
            continue

        # High density → full fidelity
        shaped.append(line)

    return shaped


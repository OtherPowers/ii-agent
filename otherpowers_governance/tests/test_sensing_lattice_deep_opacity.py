from __future__ import annotations

from datetime import datetime, timezone

from tending.field_state import FieldState
from tending.sensing_lattice import attune


def test_sensing_lattice_deep_opacity():
    """
    Deep opacity chord.

    When overlapping pressures converge, the lattice must:
    - collapse bloom
    - privilege holding / resting
    - treat silence as protective
    """

    field = FieldState(
        timestamp_utc=datetime(2025, 1, 1, 3, tzinfo=timezone.utc),
        seasons=["winter"],
        diurnal_phase="night",
    )

    lattice = attune(field)

    # posture collapses toward protection
    assert any(p in lattice.postures for p in ("holding", "resting"))

    # bloom fully evaporates
    assert lattice.bloom_conditions == []

    # silence is explicitly protective
    assert lattice.silence_is_protective is True

    # resonance carries opacity, not instruction
    joined = " ".join(lattice.resonance_notes).lower()
    assert any(
        phrase in joined
        for phrase in ("silence", "depth", "holding", "opacity")
    )


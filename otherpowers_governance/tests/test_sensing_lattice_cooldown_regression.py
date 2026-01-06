from datetime import datetime, timezone

from tending.field_state import FieldState
from tending.sensing_lattice import attune


def test_cooldown_prevents_immediate_bloom():
    """
    Cooldown regression guard.

    After a protective field state, emergence must not
    immediately reappear even when conditions soften.

    This enforces hysteresis as care.
    """

    # Protective state (night + winter)
    protected = FieldState(
        timestamp_utc=datetime(2025, 1, 1, 3, tzinfo=timezone.utc),
        seasons=["winter"],
        diurnal_phase="night",
    )

    lattice_protected = attune(protected)
    assert lattice_protected.bloom_conditions == []

    # Softer state follows immediately
    softened = FieldState(
        timestamp_utc=datetime(2025, 1, 1, 6, tzinfo=timezone.utc),
        seasons=["spring"],
        diurnal_phase="dawn",
    )

    lattice_softened = attune(softened)

    # Bloom must still not return immediately
    assert lattice_softened.bloom_conditions == []
    assert lattice_softened.silence_is_protective is True


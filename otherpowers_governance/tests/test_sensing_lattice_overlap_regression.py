from datetime import datetime, timezone

from tending.field_state import FieldState
from tending.sensing_lattice import attune


def test_bloom_evaporates_under_protective_overlap():
    """
    Overlap regression guard.

    When protective overlaps converge (winter + night),
    bloom must fully evaporate and remain absent.

    This test exists to prevent future regressions where
    'utility' quietly reappears under strain.
    """

    field = FieldState(
        timestamp_utc=datetime(2025, 1, 1, 3, tzinfo=timezone.utc),
        seasons=["winter"],
        diurnal_phase="night",
    )

    lattice = attune(field)

    # Bloom must be fully absent
    assert lattice.bloom_conditions == []

    # Protective postures must be present
    assert any(p in lattice.postures for p in ("holding", "resting"))

    # Silence is explicitly protective
    assert lattice.silence_is_protective is True


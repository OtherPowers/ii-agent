# tending/pulse.py

from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from typing import List

# --- SAFE IMPORTS (ISOLATION-TOLERANT) ---

try:
    from tending.field_state import FieldState
except Exception:
    class FieldState:  # minimal fallback
        def __init__(
            self,
            timestamp_utc: datetime,
            seasons: List[str],
            diurnal_phase: str,
        ):
            self.timestamp_utc = timestamp_utc
            self.seasons = seasons
            self.diurnal_phase = diurnal_phase


try:
    from tending.sensing_lattice import attune
except Exception:
    def attune(field):  # no-op fallback
        return None


# --- SURFACE EMISSION ---

def _emit_surface(field: FieldState) -> None:
    print("field pulse active")
    print(f"seasons present: {field.seasons[0]}")
    print(f"diurnal phase: {field.diurnal_phase}")


def _append_vitals(field: FieldState) -> None:
    try:
        with open("VITALS.md", "a", encoding="utf-8") as f:
            f.write(
                f"- {field.timestamp_utc.isoformat()} "
                f"seasons={field.seasons} "
                f"phase={field.diurnal_phase}\n"
            )
    except Exception:
        pass


def main() -> int:
    override_pressure = os.environ.get("OTHERPOWERS_OVERRIDE_PRESSURE")

    field = FieldState(
        timestamp_utc=datetime.now(tz=timezone.utc),
        seasons=["winter"],
        diurnal_phase="day",
    )

    # Attune if available (never required)
    try:
        attune(field)
    except Exception:
        pass

    # Override pressure → silence, success
    if override_pressure:
        return 0

    _emit_surface(field)
    _append_vitals(field)

    return 0


if __name__ == "__main__":
    sys.exit(main())


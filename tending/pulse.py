from __future__ import annotations

import os
from pathlib import Path
from datetime import datetime, timezone

# --- Defensive FieldState import ---------------------------------------------

try:
    from tending.field_state import FieldState  # type: ignore
except Exception:
    class FieldState:
        """
        Minimal fallback field snapshot.

        Exists solely to keep the surface executable
        when pulse is run in isolation.
        """

        def __init__(self, timestamp_utc, seasons, diurnal_phase, expressive_density=1.0):
            self.timestamp_utc = timestamp_utc
            self.seasons = seasons
            self.diurnal_phase = diurnal_phase
            self.expressive_density = expressive_density

        @classmethod
        def now(cls):
            fixed = os.environ.get("OTHERPOWERS_FIXED_TIME")
            if fixed:
                ts = datetime.fromisoformat(fixed)
            else:
                ts = datetime.now(timezone.utc)

            return cls(
                timestamp_utc=ts,
                seasons=["winter"],
                diurnal_phase="day",
                expressive_density=1.0,
            )


# --- Surface mechanics -------------------------------------------------------

def _override_pressure() -> bool:
    return os.environ.get("OTHERPOWERS_OVERRIDE_PRESSURE") is not None


def _emit_surface(field: FieldState) -> None:
    print("field pulse active")
    print(f"seasons present: {', '.join(field.seasons)}")
    print(f"diurnal phase: {field.diurnal_phase}")


def _write_vitals(field: FieldState) -> None:
    try:
        vitals = Path("VITALS.md")
        with vitals.open("a", encoding="utf-8") as f:
            f.write(
                f"{field.timestamp_utc.isoformat()} "
                f"seasons={field.seasons} "
                f"diurnal={field.diurnal_phase}\n"
            )
    except Exception:
        # Vitals must never crash the surface
        pass


def main() -> None:
    field = FieldState.now()

    if _override_pressure():
        return

    _emit_surface(field)
    _write_vitals(field)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Surface must never fail outwardly
        pass


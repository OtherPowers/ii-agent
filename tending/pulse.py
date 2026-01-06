from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import os
import sys
from typing import List


@dataclass(frozen=True)
class FieldState:
    """
    Internal field representation.

    Non-public. Safe to evolve.
    """
    timestamp_utc: datetime
    seasons: List[str]
    diurnal_phase: str


def _now_utc() -> datetime:
    fixed = os.environ.get("OTHERPOWERS_FIXED_TIME")
    if fixed:
        return datetime.fromisoformat(fixed).astimezone(timezone.utc)
    return datetime.now(timezone.utc)


def _seasons_for_time(ts: datetime) -> List[str]:
    month = ts.month
    seasons: List[str] = []

    if month in (12, 1, 2):
        seasons.append("winter")
    if month in (3, 4, 5):
        seasons.append("spring")
    if month in (6, 7, 8):
        seasons.append("summer")
    if month in (9, 10, 11):
        seasons.append("autumn")

    return seasons


def _diurnal_phase(ts: datetime) -> str:
    hour = ts.hour

    if 5 <= hour < 9:
        return "dawn"
    if 9 <= hour < 17:
        return "day"
    if 17 <= hour < 21:
        return "dusk"
    return "night"


def _compute_field_state() -> FieldState:
    now = _now_utc()
    return FieldState(
        timestamp_utc=now,
        seasons=_seasons_for_time(now),
        diurnal_phase=_diurnal_phase(now),
    )


def main() -> None:
    # Silence under override pressure
    if os.environ.get("OTHERPOWERS_OVERRIDE_PRESSURE"):
        return

    state = _compute_field_state()
    vitals = Path("VITALS.md")

    seasons_joined = ", ".join(state.seasons)

    entry = (
        "\n"
        f"## Seasonal marker — {state.timestamp_utc.replace(microsecond=0).isoformat()}\n"
        f"Seasons present: {seasons_joined}\n"
        f"Diurnal phase: {state.diurnal_phase}\n"
    )

    try:
        if vitals.exists():
            with vitals.open("a", encoding="utf-8") as f:
                f.write(entry)
        else:
            vitals.write_text(entry, encoding="utf-8")
    except Exception:
        pass

    # ✅ CANONICAL PUBLIC SURFACE (LOCKED)
    sys.stdout.write("field pulse active\n")
    sys.stdout.write(f"seasons present: {seasons_joined}\n")
    sys.stdout.write(f"diurnal phase: {state.diurnal_phase}\n")


if __name__ == "__main__":
    main()


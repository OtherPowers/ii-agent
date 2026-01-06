from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys
import os
from typing import List


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _seasons_for_time(ts: datetime) -> List[str]:
    """
    Plural, non-linear seasonal sensing.

    Multiple seasons may coexist.
    This is descriptive only.
    """
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

    # boundary overlap, intentionally non-exclusive
    if month in (2, 3):
        seasons.append("thaw")
    if month in (8, 9):
        seasons.append("heat-fade")

    # preserve order, remove duplicates
    return list(dict.fromkeys(seasons))


def main() -> None:
    # --- refraction surface ---
    # Explicit override pressure collapses emission into silence.
    if os.environ.get("OTHERPOWERS_OVERRIDE_PRESSURE"):
        return

    vitals = Path("VITALS.md")

    now = _now_utc()
    seasons = _seasons_for_time(now)
    joined = ", ".join(seasons)

    entry = (
        f"\n## Seasonal marker — {now.isoformat()}\n"
        f"Seasons present: {joined}\n"
    )

    try:
        if vitals.exists():
            with vitals.open("a", encoding="utf-8") as f:
                f.write(entry)
        else:
            vitals.write_text(entry, encoding="utf-8")
    except Exception:
        # read-only or unavailable vitals must not crash pulse
        pass

    # stdout emits only when not refracted
    sys.stdout.write(
        f"field pulse active\n"
        f"seasons present: {joined}\n"
    )


if __name__ == "__main__":
    main()


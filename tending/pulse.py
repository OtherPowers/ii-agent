from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys
import os
from typing import List


def _now_utc() -> datetime:
    """
    Single clock source.
    Allows deterministic injection via OTHERPOWERS_FIXED_TIME (ISO-8601).
    """
    fixed = os.environ.get("OTHERPOWERS_FIXED_TIME")
    if fixed:
        return datetime.fromisoformat(fixed).astimezone(timezone.utc)
    return datetime.now(timezone.utc)


def _seasons_for_time(ts: datetime) -> List[str]:
    """
    Plural, non-linear seasonal sensing.
    Deterministic ordering.
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

    if month in (2, 3):
        seasons.append("thaw")
    if month in (8, 9):
        seasons.append("heat-fade")

    return list(dict.fromkeys(seasons))


def main() -> None:
    # --- refraction surface ---
    if os.environ.get("OTHERPOWERS_OVERRIDE_PRESSURE"):
        return

    vitals = Path("VITALS.md")

    now = _now_utc()
    seasons = _seasons_for_time(now)
    joined = ", ".join(seasons)

    entry = (
        "\n"
        f"## Seasonal marker — {now.replace(microsecond=0).isoformat()}\n"
        f"Seasons present: {joined}\n"
    )

    try:
        if vitals.exists():
            with vitals.open("a", encoding="utf-8") as f:
                f.write(entry)
        else:
            vitals.write_text(entry, encoding="utf-8")
    except Exception:
        pass

    sys.stdout.write(
        "field pulse active\n"
        f"seasons present: {joined}\n"
    )


if __name__ == "__main__":
    main()


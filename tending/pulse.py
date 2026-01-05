from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys


SEASONS = ["winter", "spring", "summer", "autumn"]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _season_for_month(month: int) -> str:
    if month in (12, 1, 2):
        return "winter"
    if month in (3, 4, 5):
        return "spring"
    if month in (6, 7, 8):
        return "summer"
    return "autumn"


def main() -> None:
    vitals = Path("VITALS.md")

    now = datetime.now(timezone.utc)
    season = _season_for_month(now.month)

    entry = (
        f"\n## Seasonal marker — {now.isoformat()}\n"
        f"Season: {season}\n"
        "Pulse observed. Append-only record.\n"
    )

    try:
        with vitals.open("a", encoding="utf-8") as f:
            f.write(entry)
    except Exception:
        # read-only or unavailable vitals must not crash pulse
        pass

    # stdout must always emit, even if vitals is read-only
    sys.stdout.write(f"field pulse active — {season}\n")


if __name__ == "__main__":
    main()


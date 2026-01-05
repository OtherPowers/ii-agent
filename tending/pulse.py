"""
Seasonal Pulse for the OtherPowers ii-Agent.

This script is a periodic check-in between the codebase and the people
tending it. It does not validate, enforce, block, or decide.

It exists to:
- receive the current state of the field
- surface echoes produced by the relational substrate
- mark the passage of time
- optionally record a human reflection

Running this script is an act of presence, not compliance.
"""

from __future__ import annotations

from datetime import datetime, timezone, timedelta
from pathlib import Path

from otherpowers_governance.registry import receive_tree


SEASON_LENGTH = timedelta(days=90)
VITALS_FILE = Path("VITALS.md")


class SeasonalPulse:
    """
    A lightweight seasonal rhythm.

    This class does not determine readiness, health, or correctness.
    It simply coordinates a moment of shared attention.
    """

    def run(self) -> None:
        print("\n--- Seasonal Pulse ---\n")

        # 1. Receive the field
        print("Receiving current resonance across the field...\n")
        receive_tree()
        print("\n--- Reception complete ---\n")

        # 2. Time awareness
        last_mark = self._last_mark_time()
        now = datetime.now(timezone.utc)
        elapsed = now - last_mark

        print(f"Time since last seasonal mark: {elapsed.days} days.\n")

        # 3. Optional reflection
        if elapsed >= SEASON_LENGTH:
            self._offer_reflection()
        else:
            remaining = SEASON_LENGTH - elapsed
            print(
                "No reflection required.\n"
                f"Approximate time until next seasonal turn: {remaining.days} days.\n"
            )

    def _offer_reflection(self) -> None:
        print(
            "The season has turned.\n"
            "If you wish, you may leave a short reflection.\n"
            "Press Enter to skip.\n"
        )

        text = input("> ").strip()

        if not text:
            print("\nNo reflection recorded. The field remains open.\n")
            return

        self._record_reflection(text)
        print("\nReflection received. Thank you.\n")

    def _record_reflection(self, text: str) -> None:
        timestamp = datetime.now(timezone.utc).isoformat()

        VITALS_FILE.touch(exist_ok=True)
        with VITALS_FILE.open("a", encoding="utf-8") as f:
            f.write("\n")
            f.write(f"## Seasonal Mark — {timestamp}\n")
            f.write(f"{text}\n")

    def _last_mark_time(self) -> datetime:
        if not VITALS_FILE.exists():
            # No prior marks; return an old date to allow first reflection
            return datetime(1970, 1, 1, tzinfo=timezone.utc)

        try:
            lines = VITALS_FILE.read_text(encoding="utf-8").splitlines()
            for line in reversed(lines):
                if line.startswith("## Seasonal Mark"):
                    raw = line.split("—", 1)[1].strip()
                    return datetime.fromisoformat(raw)
        except Exception:
            pass

        return datetime(1970, 1, 1, tzinfo=timezone.utc)


if __name__ == "__main__":
    SeasonalPulse().run()


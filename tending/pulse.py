from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path


__all__ = ["main"]


class SeasonalPulse:
    """
    Non-coercive seasonal reader.

    Guarantees:
    - never blocks execution
    - never evaluates or ranks
    - always exits 0
    - safe in empty or partial environments
    """

    VITALS_FILE = Path("VITALS.md")

    SEASONS = (
        "winter",
        "summer",
    )

    def __init__(self, root: str = "otherpowers_governance"):
        self.root = root

    def run(self) -> None:
        self._emit_field_language()
        self._scan_files()
        self._tend_vitals()
        sys.exit(0)

    def _emit_field_language(self) -> None:
        print("Seasonal field reading.")
        print("Multiple seasonal states may coexist.")
        print("Current field includes:")
        for season in self.SEASONS:
            print(f"- {season}")

    def _scan_files(self) -> None:
        root = Path(self.root)
        if not root.exists():
            return
        for path in root.rglob("*.py"):
            try:
                path.read_text(encoding="utf-8")
            except Exception:
                continue

    def _tend_vitals(self) -> None:
        if not self.VITALS_FILE.exists():
            self._append_vitals("Initial seasonal marker.")

        try:
            reflection = input("").strip()
        except EOFError:
            reflection = ""

        if reflection:
            self._append_vitals(reflection)

    def _append_vitals(self, note: str) -> None:
        with self.VITALS_FILE.open("a", encoding="utf-8") as f:
            f.write("\n")
            f.write(
                f"## Seasonal marker — "
                f"{datetime.now(timezone.utc).isoformat()}\n"
            )
            f.write(note)
            f.write("\n")


def main() -> None:
    SeasonalPulse().run()


if __name__ == "__main__":
    main()


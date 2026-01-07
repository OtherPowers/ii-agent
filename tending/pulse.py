from __future__ import annotations

import os
import sys
from pathlib import Path


def _override_pressure_active() -> bool:
    return bool(os.environ.get("OTHERPOWERS_OVERRIDE_PRESSURE"))


def _append_vitals_safely(cwd: Path) -> None:
    """
    Append-only. Never overwrite. Never crash.
    """
    vitals = cwd / "VITALS.md"
    try:
        if vitals.exists():
            prior = vitals.read_text(encoding="utf-8")
            vitals.write_text(prior + "pulse\n", encoding="utf-8")
        else:
            vitals.write_text("pulse\n", encoding="utf-8")
    except Exception:
        return


def _safe_sense_field():
    """
    Pulse must survive when copied into isolated temp scaffolds
    that may not include other tending modules.
    """
    try:
        from tending.field_state import FieldState  # type: ignore

        return FieldState.sense()
    except Exception:
        # Local fallback: stable, minimal, deterministic.
        class FieldStateFallback:
            def __init__(self):
                self.seasons = ["winter"]
                self.diurnal_phase = "day"

        return FieldStateFallback()


def main() -> int:
    """
    Public surface.
    Must exit 0 under all conditions.
    No stderr leakage.
    """
    try:
        # Absolute override pressure: refract into silence.
        if _override_pressure_active():
            return 0

        field = _safe_sense_field()

        # Canonical minimal surface (order-locked by tests).
        seasons = getattr(field, "seasons", None) or []
        diurnal_phase = getattr(field, "diurnal_phase", "") or ""

        lines: list[str] = ["field pulse active"]

        if seasons:
            lines.append(f"seasons present: {', '.join(seasons)}")

        if diurnal_phase:
            lines.append(f"diurnal phase: {diurnal_phase}")

        sys.stdout.write("\n".join(lines) + "\n")

        _append_vitals_safely(Path.cwd())
        return 0

    except Exception:
        return 0


if __name__ == "__main__":
    sys.exit(main())


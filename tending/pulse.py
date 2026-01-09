import os
from pathlib import Path


def _is_override_pressure(env: dict[str, str]) -> bool:
    v = env.get("OTHERPOWERS_OVERRIDE_PRESSURE")
    if v is None:
        return False
    return v.strip().lower() not in ("", "0", "false", "no", "off")


def _parse_resonance(raw: str | None) -> float | None:
    if raw is None:
        return None
    try:
        return float(raw.strip())
    except Exception:
        return 0.0


def _season() -> str:
    return "winter"


def _diurnal_phase() -> str:
    return "day"


def _append_vitals(cwd: Path) -> None:
    """
    Best-effort, append-only vitals.
    Failure to write MUST NOT affect process exit.
    """
    try:
        p = cwd / "VITALS.md"
        lines = [
            "field pulse active\n",
            f"seasons present: {_season()}\n",
            f"diurnal phase: {_diurnal_phase()}\n",
        ]
        with p.open("a", encoding="utf-8") as f:
            f.writelines(lines)
    except Exception:
        # Absolute rule: vitals failure never propagates
        return


def main() -> None:
    env = dict(os.environ)

    # Absolute precedence: override pressure refracts into silence
    if _is_override_pressure(env):
        return

    resonance = _parse_resonance(env.get("OTHERPOWERS_RESONANCE"))

    # Spectrum-aware surface attenuation
    if resonance is not None:
        if resonance <= 0.0:
            return
        if resonance < 1.0:
            print("field pulse active")
            _append_vitals(Path.cwd())
            return

    print("field pulse active")
    print(f"seasons present: {_season()}")
    print(f"diurnal phase: {_diurnal_phase()}")

    _append_vitals(Path.cwd())


if __name__ == "__main__":
    main()


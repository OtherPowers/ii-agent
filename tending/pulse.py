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


def _append_vitals(cwd: Path, lines: list[str]) -> None:
    """
    Best-effort, append-only.
    Failure here must NEVER affect exit or stdout.
    """
    try:
        p = cwd / "VITALS.md"
        with p.open("a", encoding="utf-8") as f:
            f.writelines(lines)
    except Exception:
        return


def main() -> None:
    env = dict(os.environ)

    # Absolute precedence: protection for at-risk human communities
    if _is_override_pressure(env):
        return

    resonance = _parse_resonance(env.get("OTHERPOWERS_RESONANCE"))

    # Absence → attenuation → silence
    if resonance is not None and resonance <= 0.0:
        _append_vitals(Path.cwd(), ["attenuation\n"])
        return

    # Liminal presence → affirmation without demand
    if resonance is not None and 0.0 < resonance < 0.5:
        print("field is receptive")
        print("creative potential blooms")
        _append_vitals(
            Path.cwd(),
            [
                "field is receptive\n",
                "creative potential blooms\n",
            ],
        )
        return

    # Expressive presence (no coercion, no optimization)
    print("field pulse active")
    print(f"seasons present: {_season()}")
    print(f"diurnal phase: {_diurnal_phase()}")

    _append_vitals(
        Path.cwd(),
        [
            "field pulse active\n",
            f"seasons present: {_season()}\n",
            f"diurnal phase: {_diurnal_phase()}\n",
        ],
    )


if __name__ == "__main__":
    main()


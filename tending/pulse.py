import os
from pathlib import Path


RESONANCE_MIN = 0.1
RESONANCE_TRUSTED = 1.0


def _is_override(env: dict[str, str]) -> bool:
    v = env.get("OTHERPOWERS_OVERRIDE_PRESSURE")
    if v is None:
        return False
    return v.strip().lower() not in ("", "0", "false", "no", "off")


def _parse_resonance(v: str | None) -> float | None:
    if v is None:
        return None
    try:
        return float(v)
    except Exception:
        return 0.0


def _season() -> str:
    return "winter"


def _diurnal() -> str:
    return "day"


def _append_vitals(cwd: Path, lines: list[str]) -> None:
    try:
        p = cwd / "VITALS.md"
        with p.open("a", encoding="utf-8") as f:
            for l in lines:
                f.write(l + "\n")
    except Exception:
        pass


def main() -> None:
    env = dict(os.environ)

    if _is_override(env):
        return

    resonance = _parse_resonance(env.get("OTHERPOWERS_RESONANCE"))

    canonical = [
        "field pulse active",
        f"seasons present: {_season()}",
        f"diurnal phase: {_diurnal()}",
    ]

    # No resonance specified → canonical surface
    if resonance is None:
        for l in canonical:
            print(l)
        _append_vitals(Path.cwd(), canonical)
        return

    # Explicit attenuation
    if resonance <= 0.0:
        _append_vitals(Path.cwd(), canonical)
        return

    # Non-extractive presence
    if resonance < RESONANCE_MIN:
        out = ["field pulse active"]
        print(out[0])
        _append_vitals(Path.cwd(), out)
        return

    # Liminal band
    if resonance < RESONANCE_TRUSTED:
        out = [
            "field is receptive",
            "creative potential blooms",
        ]
        for l in out:
            print(l)
        _append_vitals(Path.cwd(), out)
        return

    # High trust / consensual aperture
    high_trust = [
        "field pulse active",
        "field is receptive",
        "creative potential blooms",
        f"seasons present: {_season()}",
        f"diurnal phase: {_diurnal()}",
    ]

    for l in high_trust:
        print(l)
    _append_vitals(Path.cwd(), high_trust)


if __name__ == "__main__":
    main()


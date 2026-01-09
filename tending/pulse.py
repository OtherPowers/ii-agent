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
    try:
        p = cwd / "VITALS.md"
        with p.open("a", encoding="utf-8") as f:
            for line in lines:
                f.write(f"{line}\n")
    except Exception:
        return


def main() -> None:
    env = dict(os.environ)

    if _is_override_pressure(env):
        return

    resonance = _parse_resonance(env.get("OTHERPOWERS_RESONANCE"))

    # Silence
    if resonance is not None and resonance <= 0.0:
        return

    # Witness mode (no resonance specified)
    if resonance is None:
        lines = [
            "field pulse active",
            f"seasons present: {_season()}",
            f"diurnal phase: {_diurnal_phase()}",
        ]
        for line in lines:
            print(line)
        _append_vitals(Path.cwd(), lines)
        return

    # Trace presence only
    if resonance < 0.3:
        lines = ["field is receptive"]
        print(lines[0])
        _append_vitals(Path.cwd(), lines)
        return

    # Liminal / consensual
    if resonance < 1.0:
        lines = [
            "field is receptive",
            "creative potential blooms",
        ]
        for line in lines:
            print(line)
        _append_vitals(Path.cwd(), lines)
        return

    # High trust / aperture widened (must include context)
    lines = [
        "field pulse active",
        "field is receptive",
        "creative potential blooms",
        f"seasons present: {_season()}",
        f"diurnal phase: {_diurnal_phase()}",
    ]
    for line in lines:
        print(line)
    _append_vitals(Path.cwd(), lines)


if __name__ == "__main__":
    main()


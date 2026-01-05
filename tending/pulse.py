"""
Seasonal Pulse for the OtherPowers ii-Agent.

This module receives the ecological texture of the repository
and offers a poly-seasonal reading.

The field may hold multiple seasons at once.
No season outranks another.
No season implies progress, delay, or deficiency.

All outputs are descriptive offerings.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from datetime import datetime, timezone

from otherpowers_governance.registry import receive_tree


# ---------------------------------
# Cyclical field language
# ---------------------------------

SEASONS = (
    "deep winter (resting field)",
    "early spring (gentle stirring)",
    "high summer (active growth)",
    "late autumn (integration and composting)",
)

VITALS_FILE = Path("VITALS.md")


# ---------------------------------
# Ecological sensing (non-linear)
# ---------------------------------

def _field_signature(root: str = "otherpowers_governance") -> str:
    """
    Produces a stable ecological signature from the field itself.

    Uses file paths only.
    No timestamps.
    No quantities.
    No activity signals.
    """
    paths = sorted(
        str(p.relative_to(root))
        for p in Path(root).rglob("*.py")
    )

    joined = "\n".join(paths).encode("utf-8")
    return hashlib.sha256(joined).hexdigest()


def _poly_season_from_signature(signature: str) -> tuple[str, str]:
    """
    Maps the field signature onto two co-present seasons.

    This allows overlapping ecological states without hierarchy.
    """
    a = int(signature[:2], 16) % len(SEASONS)
    b = int(signature[2:4], 16) % len(SEASONS)

    if a == b:
        b = (b + 1) % len(SEASONS)

    return SEASONS[a], SEASONS[b]


# ---------------------------------
# Artifact writing (descriptive only)
# ---------------------------------

def _record_vitals(seasons: tuple[str, str]) -> None:
    """
    Appends a descriptive seasonal mark to VITALS.md.

    This is not a log of behavior.
    It is a climate trace.
    """
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

    entry = (
        "\n---\n"
        f"Moment: {timestamp}\n"
        f"Field Climate:\n"
        f"- {seasons[0]}\n"
        f"- {seasons[1]}\n"
    )

    VITALS_FILE.write_text(
        VITALS_FILE.read_text() + entry
        if VITALS_FILE.exists()
        else entry,
        encoding="utf-8",
    )


# ---------------------------------
# Pulse entrypoint
# ---------------------------------

def main() -> None:
    print("\n--- Seasonal Pulse ---\n")
    print("Receiving current field conditions...\n")

    # Linguistic reception (non-authoritative)
    receive_tree()

    # Ecological reading
    signature = _field_signature()
    seasons = _poly_season_from_signature(signature)

    print("\n--- Field Climate ---\n")
    print("The field currently holds:\n")
    print(f"• {seasons[0]}")
    print(f"• {seasons[1]}\n")
    print(
        "These seasons coexist.\n"
        "Neither explains the other.\n"
        "Neither requires action.\n"
    )

    print(
        "If you wish, you may leave a short reflection.\n"
        "Press Enter to continue without offering."
    )

    try:
        reflection = input("\nReflection:\n> ").strip()
    except EOFError:
        reflection = ""

    if reflection:
        _record_vitals(seasons)
        print("\nThank you. The field has been acknowledged.\n")
    else:
        print("\nNo reflection offered. The field remains held.\n")


if __name__ == "__main__":
    main()


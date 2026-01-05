"""
Seasonal Pulse for the OtherPowers ii-Agent.

This module receives the current ecological texture of the repository
and offers a seasonal reading. It does not measure progress, enforce
norms, or imply linear advancement.

All outputs are descriptive signals only.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List

from otherpowers_governance.registry import receive_tree


# -----------------------------
# Ecological helpers
# -----------------------------

def _recent_git_activity() -> List[str]:
    """
    Returns recent commit subjects as a soft environmental trace.
    Uses git only as a terrain sensor, not an authority.
    """
    try:
        output = subprocess.check_output(
            ["git", "log", "--oneline", "-n", "12"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return [line.strip() for line in output.splitlines() if line.strip()]
    except Exception:
        return []


def _seasonal_drift(commits: List[str]) -> str:
    """
    Interprets repository motion as seasonal drift.
    This is cyclical, non-linear, and non-ordinal.
    """
    if not commits:
        return "deep winter (resting field)"

    if len(commits) <= 3:
        return "early spring (gentle stirring)"

    if len(commits) <= 8:
        return "high summer (active growth)"

    return "late autumn (integration and composting)"


# -----------------------------
# Pulse entrypoint
# -----------------------------

def main() -> None:
    print("\n--- Seasonal Pulse ---\n")
    print("Receiving current field conditions...\n")

    # Receive linguistic resonance (non-authoritative)
    receive_tree()

    # Read environmental texture
    recent = _recent_git_activity()
    season = _seasonal_drift(recent)

    print("\n--- Seasonal Reading ---\n")
    print(f"The field is in: {season}.")
    print(
        "This is a descriptive rhythm, not an evaluation.\n"
        "If it resonates, you may leave a short reflection.\n"
        "Press Enter to continue without offering."
    )

    try:
        input("\nReflection:\n> ")
    except EOFError:
        pass


if __name__ == "__main__":
    main()


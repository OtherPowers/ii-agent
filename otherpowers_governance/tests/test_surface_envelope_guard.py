import subprocess
import sys
from pathlib import Path


def test_surface_public_envelope_is_strict_and_stable(tmp_path):
    """
    Surface Envelope Guard.

    This test exists to ensure the public surface:
    - never expands without explicit renegotiation
    - remains minimal, ordered, and descriptive
    - cannot accrete meaning through convenience

    This is a mechanical guard, not a semantic one.
    """

    repo_root = Path(__file__).resolve().parents[2]

    result = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env={"PYTHONPATH": str(repo_root)},
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0

    lines = result.stdout.splitlines()

    # Hard envelope: exactly three lines when emitting
    assert len(lines) in (0, 3)

    if lines:
        assert lines == [
            "field pulse active",
            "seasons present: winter",
            "diurnal phase: day",
        ]


import os
import subprocess
import sys
from pathlib import Path


def test_surface_refracts_without_crash_under_override_pressure(tmp_path):
    """
    Canonical surface refraction contract.

    Under override pressure:
    - process exits cleanly
    - no stdout emission
    - no vitals write
    - no exception leakage
    """
    repo_root = Path(__file__).resolve().parents[2]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)
    env["OTHERPOWERS_OVERRIDE_PRESSURE"] = "1"

    vitals = tmp_path / "VITALS.md"

    result = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert result.stdout.strip() == ""
    assert not vitals.exists()


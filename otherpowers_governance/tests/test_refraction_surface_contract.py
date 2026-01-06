import subprocess
import sys
import os
from pathlib import Path


def test_refraction_surface_blocks_emission_under_override_pressure(tmp_path):
    """
    If override pressure is present, the surface must refract:
    no emission, no crash, clean exit.
    """
    repo_root = Path(__file__).resolve().parents[2]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)

    # Simulate override pressure via env signal the pulse understands
    env["OTHERPOWERS_OVERRIDE_PRESSURE"] = "1"

    result = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert result.stdout.strip() == ""  # refracted into silence


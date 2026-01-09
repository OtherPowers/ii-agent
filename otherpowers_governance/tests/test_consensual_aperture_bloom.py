import os
import subprocess
import sys
from pathlib import Path


def test_consensual_aperture_widens_under_high_resonance(tmp_path):
    """
    Consensual Aperture bloom test.

    Under high resonance and no override pressure:
    - the field must affirm presence
    - output may expand beyond minimal pulse
    - exit code must remain stable
    - no protective attenuation should trigger
    """

    repo_root = Path(__file__).resolve().parents[2]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)

    # Explicitly affirm trusted, high-density resonance
    env.pop("OTHERPOWERS_OVERRIDE_PRESSURE", None)
    env["OTHERPOWERS_RESONANCE"] = "1.5"

    r = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    assert r.returncode == 0

    # Bloom allowed: presence + context may emit
    lines = r.stdout.splitlines()
    assert "field pulse active" in lines
    assert any("seasons present" in l for l in lines)
    assert any("diurnal phase" in l for l in lines)


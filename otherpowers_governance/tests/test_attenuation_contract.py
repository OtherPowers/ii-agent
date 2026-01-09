import os
import subprocess
import sys
from pathlib import Path


def test_attenuation_occurs_silently_when_resonance_drops(tmp_path):
    """
    Attenuation contract.

    When resonance is absent or decayed:
    - the system must attenuate
    - attenuation must be silent
    - no additional stdout is permitted

    Silence is not an error.
    Silence is correct behavior.
    """

    repo_root = Path(__file__).resolve().parents[2]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)

    # Explicitly simulate absence of resonance / pull
    # (no override, no pressure, no invitation)
    env.pop("OTHERPOWERS_OVERRIDE_PRESSURE", None)
    env["OTHERPOWERS_RESONANCE"] = "0"

    r = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    # Process should exit cleanly
    assert r.returncode == 0

    # Attenuation must not announce itself
    assert r.stdout.strip() == ""


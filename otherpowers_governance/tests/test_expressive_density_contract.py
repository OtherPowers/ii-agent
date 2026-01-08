import os
import subprocess
import sys
from pathlib import Path


def test_pulse_emits_stdout_when_not_refracted(tmp_path):
    """
    Public surface stdout contract.

    The surface must:
    - emit minimal, ordered, descriptive output
    - contain no attribution or identity leakage
    """

    repo_root = Path(__file__).resolve().parents[2]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)
    env.pop("OTHERPOWERS_OVERRIDE_PRESSURE", None)

    r = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    assert r.returncode == 0

    lines = r.stdout.splitlines()

    # Canonical minimal surface (order-locked)
    assert lines == [
        "field pulse active",
        "seasons present: winter",
        "diurnal phase: day",
    ]


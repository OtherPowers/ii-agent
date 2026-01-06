"""
Surface Vow: Idempotence under identical conditions.

If the same invocation is run under truly identical starting fields,
the surface must yield identical emissions.

Reliability is a form of care.
"""

import subprocess
import sys
import os
from pathlib import Path


def test_surface_idempotence_under_identical_conditions(tmp_path):
    """
    Identical conditions must yield identical outcomes.
    """
    repo_root = Path(__file__).resolve().parents[2]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)

    run1 = tmp_path / "run1"
    run2 = tmp_path / "run2"
    run1.mkdir()
    run2.mkdir()

    r1 = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=run1,
        env=env,
        capture_output=True,
        text=True,
    )

    r2 = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=run2,
        env=env,
        capture_output=True,
        text=True,
    )

    assert r1.returncode == 0
    assert r2.returncode == 0
    assert r1.stdout == r2.stdout
    assert r1.stderr == r2.stderr

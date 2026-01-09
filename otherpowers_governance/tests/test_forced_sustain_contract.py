# File: otherpowers_governance/tests/test_forced_sustain_contract.py

import os
import subprocess
import sys
from pathlib import Path


def test_utility_does_not_sustain_without_resonance(tmp_path):
    """
    Forced sustain contract.

    When resonance is absent:
    - the utility must not sustain activity
    - no stdout should be emitted
    - the process must exit cleanly

    Persistence without pull is a violation.
    """

    repo_root = Path(__file__).resolve().parents[2]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)

    # Explicit absence of resonance
    env.pop("OTHERPOWERS_OVERRIDE_PRESSURE", None)
    env["OTHERPOWERS_RESONANCE"] = "0"

    r = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    assert r.returncode == 0
    assert r.stdout.strip() == ""


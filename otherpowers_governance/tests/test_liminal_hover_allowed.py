# File: otherpowers_governance/tests/test_liminal_hover_allowed.py

import os
import subprocess
import sys
from pathlib import Path


def test_liminal_hover_allows_presence_without_escalation(tmp_path):
    """
    Liminal hover allowance.

    Hovering, signaling, and clustering are valid states.
    Presence does not require action.
    """

    repo_root = Path(__file__).resolve().parents[2]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)
    env.pop("OTHERPOWERS_OVERRIDE_PRESSURE", None)
    env["OTHERPOWERS_RESONANCE"] = "0.3"

    r = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    assert r.returncode == 0
    assert r.stdout.strip() in ("", "field pulse active")


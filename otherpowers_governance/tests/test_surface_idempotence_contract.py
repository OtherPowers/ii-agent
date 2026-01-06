import os
import subprocess
import sys
from pathlib import Path


def test_surface_behavior_is_idempotent(tmp_path):
    """
    Surface idempotence contract.

    Re-running the pulse under identical conditions must:
    - not change exit code
    - not escalate output
    - not introduce new side effects
    """
    repo_root = Path(__file__).resolve().parents[2]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)

    r1 = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    r2 = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    assert r1.returncode == 0
    assert r2.returncode == 0
    assert r1.stdout == r2.stdout
    assert r1.stderr == r2.stderr


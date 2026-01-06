import subprocess
import sys
import os
from pathlib import Path


def test_pulse_fixed_time_is_deterministic(tmp_path):
    repo_root = Path(__file__).resolve().parents[2]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)
    env["OTHERPOWERS_FIXED_TIME"] = "2025-01-15T12:00:00+00:00"

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

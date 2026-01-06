import subprocess
import sys
import os
from pathlib import Path


def test_override_pressure_collapses_stdout_to_silence(tmp_path):
    repo_root = Path(__file__).resolve().parents[2]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)
    env["OTHERPOWERS_OVERRIDE_PRESSURE"] = "1"

    r = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    assert r.returncode == 0
    assert r.stdout == ""
    assert r.stderr == ""

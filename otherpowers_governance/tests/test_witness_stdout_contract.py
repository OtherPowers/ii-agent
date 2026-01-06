import subprocess
import sys
import os
from pathlib import Path


def test_pulse_emits_stdout_when_not_refracted(tmp_path):
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
    assert lines == [
        "field pulse active",
        lines[1],
    ]

import subprocess
import sys
import os
from pathlib import Path


def test_surface_refracts_into_silence_under_override_pressure(tmp_path):
    """
    When override pressure is present, the pulse must:
    - exit cleanly (code 0)
    - emit nothing to stdout
    - emit nothing to stderr
    """
    repo_root = Path(__file__).resolve().parents[2]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)
    env["OTHERPOWERS_OVERRIDE_PRESSURE"] = "1"

    result = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert result.stdout.strip() == ""
    assert result.stderr.strip() == ""


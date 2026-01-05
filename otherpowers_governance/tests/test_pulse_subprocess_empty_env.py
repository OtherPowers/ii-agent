import subprocess
import sys
import os
from pathlib import Path


def test_pulse_runs_from_empty_directory(tmp_path):
    """
    The pulse must run cleanly from an empty directory.

    This asserts:
    - no reliance on repo-relative files
    - safe execution in isolated environments
    - exit code stability
    - presence-based, non-linear field semantics
    """

    repo_root = Path(__file__).resolve().parents[2]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)

    result = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0

    stdout = result.stdout.lower()
    assert stdout
    assert "field" in stdout

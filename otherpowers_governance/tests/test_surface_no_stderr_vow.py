import subprocess
import sys
import os
from pathlib import Path


def test_surface_emits_no_stderr(tmp_path):
    """
    The surface must not leak internal friction.
    stderr remains empty under normal operation.
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
    assert result.stderr.strip() == ""


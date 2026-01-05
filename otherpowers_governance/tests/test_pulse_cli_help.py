import subprocess
import sys
import os
from pathlib import Path


def test_pulse_help_is_safe_noop(tmp_path):
    repo_root = Path(__file__).resolve().parents[2]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)

    result = subprocess.run(
        [sys.executable, "-m", "tending.pulse", "--help"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    # must not block or error
    assert result.returncode == 0

    # stdout may be empty or minimal; presence-only
    # no assertions on wording


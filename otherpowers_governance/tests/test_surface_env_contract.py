import os
import subprocess
import sys
from pathlib import Path


def test_surface_env_signals_do_not_leak_or_crash(tmp_path):
    """
    Surface environment contract.

    Env signals may influence posture,
    but must never:
    - crash the process
    - emit env values
    - create side effects beyond posture
    """
    repo_root = Path(__file__).resolve().parents[2]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)
    env["OTHERPOWERS_OVERRIDE_PRESSURE"] = "1"
    env["OTHERPOWERS_INTERNAL_ONLY"] = "secret_should_not_leak"

    result = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0

    # no env leakage to stdout or stderr
    combined = (result.stdout + result.stderr).lower()
    assert "override_pressure" not in combined
    assert "internal_only" not in combined
    assert "secret" not in combined


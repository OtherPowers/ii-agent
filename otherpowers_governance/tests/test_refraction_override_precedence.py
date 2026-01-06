import subprocess
import sys
import os
from pathlib import Path


def test_override_pressure_has_precedence_over_all_emission(tmp_path):
    """
    Override pressure is absolute.

    When present, NOTHING emits:
    - no stdout
    - no stderr
    - no vitals write
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
    assert not (tmp_path / "VITALS.md").exists()


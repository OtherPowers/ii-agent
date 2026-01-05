import subprocess
import sys
from pathlib import Path


def test_pulse_cli_runs_and_exits_zero(tmp_path):
    """
    Pulse must be runnable as a module and exit cleanly.
    """
    repo_root = Path(__file__).resolve().parents[2]

    result = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env={"PYTHONPATH": str(repo_root)},
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert result.stdout


def test_pulse_does_not_crash_without_vitals(tmp_path):
    """
    Pulse must tolerate missing files and empty environments.
    """
    repo_root = Path(__file__).resolve().parents[2]

    result = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env={"PYTHONPATH": str(repo_root)},
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0


import subprocess
import sys
from pathlib import Path


def test_seasonal_pulse_runs_cleanly():
    """
    Smoke test: the seasonal pulse runs without crashing.
    """

    repo_root = Path(__file__).resolve().parents[2]

    result = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=repo_root,
        input="\n",
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0


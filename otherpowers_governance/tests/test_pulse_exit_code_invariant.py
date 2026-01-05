import subprocess
import sys
import os
from pathlib import Path


def test_pulse_respects_silence_as_success(tmp_path):
    repo_root = Path(__file__).resolve().parents[2]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)

    args_sets = [
        [],
        ["--help"],
        ["--unknown"],
        ["--foo", "bar"],
        ["--", "--still-not-real"],
    ]

    for args in args_sets:
        result = subprocess.run(
            [sys.executable, "-m", "tending.pulse", *args],
            cwd=tmp_path,
            env=env,
            capture_output=True,
            text=True,
        )

        # Silence or non-action is a valid outcome.
        # Exit code 0 asserts intentional restraint, not failure.
        assert result.returncode == 0


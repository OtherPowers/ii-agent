import subprocess
import sys
import os
from pathlib import Path


def test_pulse_stdout_contract_presence_only(tmp_path):
    """
    The pulse must emit *something* meaningful, without enforcing verbosity,
    linear narrative, or specific phrasing.

    This test asserts presence, not interpretation.
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

    # 1. Process exits cleanly
    assert result.returncode == 0

    # 2. Some stdout is emitted
    stdout = result.stdout.strip()
    assert stdout != ""

    lowered = stdout.lower()

    # 3. Output references the field without enforcing taxonomy
    assert any(
        token in lowered
        for token in [
            "field",
            "season",
            "stasis",
            "presence",
            "pulse",
        ]
    )


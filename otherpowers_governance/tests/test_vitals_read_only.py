import subprocess
import sys
import os
from pathlib import Path


def test_pulse_survives_read_only_vitals(tmp_path):
    vitals = tmp_path / "VITALS.md"
    vitals.write_text("existing lineage\n")
    vitals.chmod(0o444)  # read-only

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
    assert vitals.read_text() == "existing lineage\n"


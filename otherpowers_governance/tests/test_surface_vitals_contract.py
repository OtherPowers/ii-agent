import os
import subprocess
import sys
from pathlib import Path


def test_vitals_append_only_without_override_pressure(tmp_path):
    """
    Surface vitals contract.

    Without override pressure:
    - process exits cleanly
    - stdout may emit
    - VITALS.md is created or appended (never overwritten)
    """
    repo_root = Path(__file__).resolve().parents[2]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)

    vitals = tmp_path / "VITALS.md"

    r1 = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )
    assert r1.returncode == 0
    assert vitals.exists()

    first = vitals.read_text(encoding="utf-8")

    r2 = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )
    assert r2.returncode == 0

    second = vitals.read_text(encoding="utf-8")

    assert first in second
    assert len(second) > len(first)


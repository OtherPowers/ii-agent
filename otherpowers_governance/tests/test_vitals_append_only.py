import subprocess
import sys
import os
from pathlib import Path


def test_vitals_is_append_only_across_runs(tmp_path):
    """
    VITALS.md must be append-only.

    This asserts:
    - file is created if missing
    - subsequent runs append, not overwrite
    - prior content is preserved
    """

    vitals = tmp_path / "VITALS.md"

    repo_root = Path(__file__).resolve().parents[2]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)

    # first run
    r1 = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )
    assert r1.returncode == 0
    assert vitals.exists()

    first_content = vitals.read_text()

    # second run
    r2 = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )
    assert r2.returncode == 0

    second_content = vitals.read_text()

    assert first_content in second_content
    assert len(second_content) > len(first_content)


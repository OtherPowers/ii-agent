import subprocess
import sys
import os
from pathlib import Path


def test_field_emission_format_is_stable(tmp_path):
    """
    Field emission must be line-stable and order-stable.
    No drift, no extra whitespace, no locale bleed.
    """
    repo_root = Path(__file__).resolve().parents[2]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)

    r = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    assert r.returncode == 0

    lines = r.stdout.splitlines()

    assert lines[0] == "field pulse active"
    assert lines[1].startswith("seasons present: ")
    assert len(lines) == 2

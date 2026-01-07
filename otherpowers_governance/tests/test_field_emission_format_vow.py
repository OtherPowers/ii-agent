import os
import subprocess
import sys
from pathlib import Path


def test_field_emission_format_is_stable(tmp_path):
    """
    Field emission must be line-stable and order-stable.

    This test guards against:
    - drift in ordering
    - accidental removal of required lines
    - expansion of meaning through re-interpretation

    It does NOT own the canonical surface schema.
    That responsibility lives in test_field_surface_schema.py
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

    # minimal ordering guarantees
    assert lines[0] == "field pulse active"
    assert lines[1].startswith("seasons present: ")

    # do not assert exact length here
    # schema authority lives elsewhere
    assert len(lines) >= 2


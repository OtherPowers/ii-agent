import os
import subprocess
import sys
from pathlib import Path


def test_field_surface_schema_is_minimal_and_stable(tmp_path):
    """
    Field surface schema invariant.

    The public field surface must remain:
    - minimal
    - order-stable
    - non-expansive
    - free of analytic / behavioral leakage
    """
    repo_root = Path(__file__).resolve().parents[2]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)
    env.pop("OTHERPOWERS_OVERRIDE_PRESSURE", None)

    r = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    assert r.returncode == 0

    lines = r.stdout.splitlines()

    # fixed minimal surface
    assert lines[0] == "field pulse active"
    assert lines[1].startswith("seasons present: ")
    assert lines[2].startswith("diurnal phase: ")

    # no silent expansion
    assert len(lines) == 3


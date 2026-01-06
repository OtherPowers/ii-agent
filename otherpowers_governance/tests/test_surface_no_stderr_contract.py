import os
import subprocess
import sys
from pathlib import Path


def test_surface_never_emits_stderr(tmp_path):
    """
    Surface stderr contract.

    The surface must never leak intent, pressure, or internal state
    through stderr. All refraction resolves into silence or stdout.
    """
    repo_root = Path(__file__).resolve().parents[2]

    base_env = os.environ.copy()
    base_env["PYTHONPATH"] = str(repo_root)

    # normal run
    r1 = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=base_env,
        capture_output=True,
        text=True,
    )
    assert r1.returncode == 0
    assert r1.stderr.strip() == ""

    # override pressure
    env_override = base_env.copy()
    env_override["OTHERPOWERS_OVERRIDE_PRESSURE"] = "1"

    r2 = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=env_override,
        capture_output=True,
        text=True,
    )
    assert r2.returncode == 0
    assert r2.stderr.strip() == ""


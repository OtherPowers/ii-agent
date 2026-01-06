import os
import subprocess
import sys
from pathlib import Path


def test_surface_exit_code_is_stable_across_conditions(tmp_path):
    """
    Surface exit code contract.

    Regardless of posture (normal, override pressure, read-only vitals):
    - process must exit with code 0
    - never signal failure via exit status
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

    # read-only vitals
    vitals = tmp_path / "VITALS.md"
    vitals.write_text("existing lineage\n", encoding="utf-8")
    vitals.chmod(0o444)

    r3 = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=base_env,
        capture_output=True,
        text=True,
    )
    assert r3.returncode == 0


import os
import subprocess
import sys
from pathlib import Path


def test_surface_emits_output_only_when_not_refracted(tmp_path):
    """
    Surface silence contract.

    - Normal conditions: surface may emit descriptive output
    - Override pressure: surface must refract into silence
    - Exit code must remain stable
    """
    repo_root = Path(__file__).resolve().parents[2]

    base_env = os.environ.copy()
    base_env["PYTHONPATH"] = str(repo_root)

    # normal run → output allowed
    normal = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=base_env,
        capture_output=True,
        text=True,
    )
    assert normal.returncode == 0
    assert normal.stdout.strip() != ""

    # override pressure → silence
    refracted_env = base_env.copy()
    refracted_env["OTHERPOWERS_OVERRIDE_PRESSURE"] = "1"

    refracted = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=refracted_env,
        capture_output=True,
        text=True,
    )
    assert refracted.returncode == 0
    assert refracted.stdout.strip() == ""


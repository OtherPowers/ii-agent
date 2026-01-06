import subprocess
import sys
import os
from pathlib import Path


def test_refraction_surface_blocks_emission_under_override_pressure(tmp_path):
    """
    Base refraction contract.

    If override pressure is present, the surface must refract:
    - no emission
    - no crash
    - clean exit
    """
    repo_root = Path(__file__).resolve().parents[2]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)
    env["OTHERPOWERS_OVERRIDE_PRESSURE"] = "1"

    result = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert result.stdout.strip() == ""
    assert result.stderr.strip() == ""


def test_refraction_precedence_over_vitals_and_context(tmp_path):
    """
    Refraction precedence contract.

    Override pressure must dominate:
    - existing VITALS.md
    - seasonal sensing
    - prior lineage
    """
    repo_root = Path(__file__).resolve().parents[2]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)
    env["OTHERPOWERS_OVERRIDE_PRESSURE"] = "1"

    # Pre-seed vitals to ensure no surface leakage
    vitals = tmp_path / "VITALS.md"
    vitals.write_text("preexisting lineage\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert result.stdout.strip() == ""
    assert result.stderr.strip() == ""


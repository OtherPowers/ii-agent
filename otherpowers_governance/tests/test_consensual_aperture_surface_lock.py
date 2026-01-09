import os
import subprocess
import sys
from pathlib import Path


def test_consensual_aperture_surface_is_ordered_and_bounded(tmp_path):
    """
    Consensual Aperture surface lock.

    Under high trust:
    - bloom is allowed
    - context is allowed
    - surface must still remain bounded and ordered
    - no semantic sprawl may occur
    """

    repo_root = Path(__file__).resolve().parents[2]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)
    env["OTHERPOWERS_RESONANCE"] = "2.0"
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

    # Required anchors
    assert lines[0] == "field pulse active"
    assert "field is receptive" in lines
    assert "creative potential blooms" in lines

    # Context must appear after affirmation, never before
    season_idx = next(i for i, l in enumerate(lines) if l.startswith("seasons present"))
    bloom_idx = lines.index("creative potential blooms")
    assert season_idx > bloom_idx

    # Hard ceiling
    assert len(lines) <= 5


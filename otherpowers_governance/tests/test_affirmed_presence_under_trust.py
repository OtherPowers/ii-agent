import os
import sys
import subprocess
from pathlib import Path


def test_affirmed_presence_when_conditions_are_non_extractive(tmp_path):
    """
    Affirmed Presence invariant.

    When:
    - no override pressure is present
    - resonance is present but not coercive

    The field may:
    - affirm presence
    - name bloom as possibility
    - remain minimal and non-directive
    """

    repo_root = Path(__file__).resolve().parents[2]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)
    env.pop("OTHERPOWERS_OVERRIDE_PRESSURE", None)

    # Liminal, consensual resonance
    env["OTHERPOWERS_RESONANCE"] = "0.4"

    r = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    assert r.returncode == 0

    assert r.stdout.strip() in (
        "",
        "field is receptive\ncreative potential blooms",
    )


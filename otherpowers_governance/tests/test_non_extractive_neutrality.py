import os
import subprocess
import sys
from pathlib import Path


def test_non_extractive_activity_does_not_accumulate_capacity(tmp_path):
    """
    Non-extractive neutrality test.

    When activity is present without sufficient resonance:
    - presence may be affirmed
    - the field must not escalate into bloom
    - no expanded contextual emission is permitted
    - exit must remain clean

    Harmful or extractive dynamics are neutralized
    through lack of accumulation, not punishment.
    """

    repo_root = Path(__file__).resolve().parents[2]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)

    # Simulate activity without sufficient resonance
    env.pop("OTHERPOWERS_OVERRIDE_PRESSURE", None)
    env["OTHERPOWERS_RESONANCE"] = "0.05"

    r = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    assert r.returncode == 0

    lines = r.stdout.splitlines()

    # Allowed: soft affirmation of presence
    allowed = {
        "field pulse active",
        "field is receptive",
    }

    # Explicitly disallowed: bloom / expansion language
    disallowed = {
        "creative potential blooms",
        "capacity expands",
        "collective bloom active",
    }

    for line in lines:
        assert line in allowed
        assert line not in disallowed


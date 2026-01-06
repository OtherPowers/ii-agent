import subprocess
import sys
import os
from pathlib import Path


def test_pulse_ignores_locale_and_tz(tmp_path):
    repo_root = Path(__file__).resolve().parents[2]

    base_env = os.environ.copy()
    base_env["PYTHONPATH"] = str(repo_root)
    base_env["OTHERPOWERS_FIXED_TIME"] = "2025-06-01T00:00:00+00:00"

    env_a = base_env.copy()
    env_a["TZ"] = "UTC"
    env_a["LC_ALL"] = "C"

    env_b = base_env.copy()
    env_b["TZ"] = "America/Los_Angeles"
    env_b["LC_ALL"] = "fr_FR.UTF-8"

    dir_a = tmp_path / "a"
    dir_b = tmp_path / "b"
    dir_a.mkdir()
    dir_b.mkdir()

    r1 = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=dir_a,
        env=env_a,
        capture_output=True,
        text=True,
    )

    r2 = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        cwd=dir_b,
        env=env_b,
        capture_output=True,
        text=True,
    )

    assert r1.returncode == 0
    assert r2.returncode == 0
    assert r1.stdout == r2.stdout
    assert r1.stderr == r2.stderr

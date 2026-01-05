import subprocess
import sys
from pathlib import Path


def test_seasonal_pulse_runs_cleanly(tmp_path, monkeypatch):
    """
    The seasonal pulse should:

    - execute without raising
    - be runnable as a module
    - tolerate empty or minimal environments
    - describe field states without assuming linear progress
    - allow multiple seasonal states to coexist
    """

    # Isolate execution
    monkeypatch.chdir(tmp_path)

    # Minimal scaffold expected by the pulse
    (tmp_path / "tending").mkdir(parents=True)
    (tmp_path / "otherpowers_governance").mkdir(parents=True)

    # Copy pulse module into isolated environment
    source_root = Path(__file__).resolve().parents[2]
    pulse_src = source_root / "tending" / "pulse.py"
    pulse_dst = tmp_path / "tending" / "pulse.py"
    pulse_dst.write_text(pulse_src.read_text(encoding="utf-8"), encoding="utf-8")

    # Ensure module visibility
    (tmp_path / "tending" / "__init__.py").write_text("", encoding="utf-8")

    # Run the pulse, skipping optional reflection
    result = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        input="\n",
        text=True,
        capture_output=True,
    )

    # 1. Process completes without crashing
    assert result.returncode == 0

    output = result.stdout.lower()

    # 2. Seasonal language is descriptive, not linear
    assert "season" in output or "field" in output

    # 3. Non-linear coexistence is allowed
    # (e.g. more than one seasonal state may appear)
    seasonal_markers = [
        "winter",
        "summer",
        "spring",
        "autumn",
    ]
    found = [s for s in seasonal_markers if s in output]
    assert len(found) >= 1

    # 4. No demand for reflection
    assert "required" not in output


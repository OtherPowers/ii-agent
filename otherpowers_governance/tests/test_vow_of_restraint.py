import subprocess
import sys


def test_vow_of_restraint():
    """
    ABI VOW — The Right to Be Small

    The public surface must never exceed the Triad of Presence.
    Silence (0 lines) is a valid outcome.
    """

    result = subprocess.run(
        [sys.executable, "-m", "tending.pulse"],
        capture_output=True,
        text=True,
    )

    # Extract non-empty stdout lines
    lines = [line for line in result.stdout.splitlines() if line.strip()]

    # The Vow: at most three lines
    assert len(lines) <= 3, (
        f"Threshold violation: surface expanded to {len(lines)} lines."
    )

    # If present, ensure the Triad remains unpolluted
    if len(lines) >= 1:
        assert lines[0].startswith("field pulse active")


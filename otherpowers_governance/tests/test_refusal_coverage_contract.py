from pathlib import Path


def test_every_refusal_invariant_has_coverage():
    """
    Ensures refusal coverage stays complete.

    Coverage is behavioral, not filename-based:
    an invariant counts if any test asserts refusal
    via require_not_in_stasis or StasisEncountered.
    """
    tests_dir = Path(__file__).parent

    expected = {
        "no_forced_synthesis",
        "no_override_pressure",
        "no_extractive_logging",
        "no_identity_leakage",
        "no_surveillance_escalation",
        "no_scope_creep",
    }

    found = set()

    for p in tests_dir.glob("test_*.py"):
        text = p.read_text(encoding="utf-8")

        if "require_not_in_stasis" in text or "StasisEncountered" in text:
            for inv in expected:
                if inv in text:
                    found.add(inv)

    assert expected.issubset(found)


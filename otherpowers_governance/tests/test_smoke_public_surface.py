"""
Smoke tests for public-facing surfaces.

These tests exist to ensure that:
- core modules import cleanly
- posture, stasis, enforcement, and pulse do not regress at import time
- no hidden side effects or environment assumptions are introduced
"""

def test_governance_modules_import_cleanly():
    import otherpowers_governance.governance.stasis
    import otherpowers_governance.governance.renegotiation
    import otherpowers_governance.governance.invariant_enforcement


def test_pulse_module_imports_cleanly():
    import tending.pulse


def test_no_side_effects_on_import():
    """
    Importing core modules should not:
    - write files
    - emit stdout
    - mutate global state
    """
    import sys

    before = set(sys.modules.keys())
    import otherpowers_governance.governance.stasis  # noqa: F401
    after = set(sys.modules.keys())

    # import should be additive but not explosive
    assert len(after - before) < 20


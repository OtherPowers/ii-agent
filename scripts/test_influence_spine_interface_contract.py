"""
Interface contract tests for InfluenceSpineAdapter.

These tests lock the behavioral surface of the adapter so future
changes cannot silently alter expectations around spines, posture
memory, or mutation.

Canonical rule:
- Silence is valid.
- Non-callable spines without .process() are allowed and simply emit nothing.
"""

import pytest

from otherpowers_governance.intelligence.influence_spine_adapter import (
    InfluenceSpineAdapter,
)


# --- helpers -----------------------------------------------------------------


class _ValidSpine:
    def process(self, context):
        return {"posture": "open"}


class _SilentSpine:
    """Intentionally silent spine (no __call__, no .process)."""
    pass


# --- tests -------------------------------------------------------------------


def test_adapter_accepts_spine_with_process_method():
    adapter = InfluenceSpineAdapter(spine=_ValidSpine())
    out = adapter.process({})

    # may emit or may return None depending on governance,
    # but must not error
    assert out is None or isinstance(out, dict)


def test_adapter_allows_silent_spine():
    adapter = InfluenceSpineAdapter(spine=_SilentSpine())
    out = adapter.process({})

    # silence is valid
    assert out is None


def test_posture_snapshot_returns_new_object_each_call():
    adapter = InfluenceSpineAdapter(spine=_ValidSpine())

    adapter.process({})
    snap1 = adapter.posture_snapshot()
    snap2 = adapter.posture_snapshot()

    assert snap1 is not snap2
    assert snap1.posture == snap2.posture
    assert snap1.weight == snap2.weight


def test_adapter_does_not_mutate_input_context():
    adapter = InfluenceSpineAdapter(spine=_ValidSpine())

    context = {"a": 1, "b": {"nested": True}}
    adapter.process(context)

    # shallow + nested integrity
    assert context == {"a": 1, "b": {"nested": True}}


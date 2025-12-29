"""
Emission boundary contract for InfluenceSpineAdapter.

This contract fixes the non-amplification invariant:
- emission may occur at most once per adapter lifecycle
- silence is a complete outcome
- repeated inputs do not accumulate force
"""

from otherpowers_governance.intelligence.influence_spine_adapter import (
    InfluenceSpineAdapter,
)


# --- helpers -----------------------------------------------------------------


class _AlwaysEmittingSpine:
    def __call__(self, context):
        return {"posture": "open"}


class _SilentSpine:
    def __call__(self, context):
        return None


class _RecordingBridge:
    def __init__(self):
        self.calls = 0
        self.payloads = []

    def emit(self, summary):
        self.calls += 1
        self.payloads.append(summary)
        return summary


# --- tests -------------------------------------------------------------------


def test_emission_occurs_at_most_once():
    adapter = InfluenceSpineAdapter(spine=_AlwaysEmittingSpine())
    bridge = _RecordingBridge()
    adapter._bridge = bridge

    adapter.process({})
    adapter.process({})
    adapter.process({})

    assert bridge.calls == 1
    assert len(bridge.payloads) == 1


def test_silence_never_triggers_emission():
    adapter = InfluenceSpineAdapter(spine=_SilentSpine())
    bridge = _RecordingBridge()
    adapter._bridge = bridge

    adapter.process({})
    adapter.process({})
    adapter.process({})

    assert bridge.calls == 0
    assert bridge.payloads == []


def test_emission_does_not_depend_on_input_variation():
    adapter = InfluenceSpineAdapter(spine=_AlwaysEmittingSpine())
    bridge = _RecordingBridge()
    adapter._bridge = bridge

    adapter.process({"a": 1})
    adapter.process({"a": 2})
    adapter.process({"a": 3})

    assert bridge.calls == 1


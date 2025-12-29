"""
Emission boundary contract tests for InfluenceSpineAdapter.

This contract guarantees:
- Silence is valid and non-failing
- Emission occurs at most once per adapter lifecycle
- Repeated calls do not amplify force
- Posture accumulation does not affect emission boundaries
"""

from otherpowers_governance.intelligence.influence_spine_adapter import (
    InfluenceSpineAdapter,
)


# --- helpers -----------------------------------------------------------------


class _SilentSpine:
    def __call__(self, context):
        return None


class _EmittingSpine:
    def __init__(self):
        self.calls = 0

    def __call__(self, context):
        self.calls += 1
        return {"posture": "open"}


class _RecordingBridge:
    def __init__(self):
        self.calls = 0
        self.payloads = []

    def emit(self, payload):
        self.calls += 1
        self.payloads.append(payload)
        return payload


# --- tests -------------------------------------------------------------------


def test_silence_is_valid_and_non_emissive():
    adapter = InfluenceSpineAdapter(spine=_SilentSpine())

    out1 = adapter.process({})
    out2 = adapter.process({})

    assert out1 is None
    assert out2 is None


def test_emission_occurs_at_most_once():
    spine = _EmittingSpine()
    adapter = InfluenceSpineAdapter(spine=spine)

    bridge = _RecordingBridge()
    adapter._bridge = bridge  # explicit override for test control

    out1 = adapter.process({})
    out2 = adapter.process({})
    out3 = adapter.process({})

    assert out1 is not None
    assert out2 is None
    assert out3 is None

    assert bridge.calls == 1
    assert spine.calls >= 1  # spine may be invoked; emission must not amplify


def test_posture_accumulation_does_not_bypass_emission_boundary():
    spine = _EmittingSpine()
    adapter = InfluenceSpineAdapter(spine=spine)

    bridge = _RecordingBridge()
    adapter._bridge = bridge

    adapter.process({})
    adapter.process({})
    adapter.process({})

    snap = adapter.posture_snapshot()

    assert bridge.calls == 1
    assert snap.posture == "open"
    assert snap.weight >= 1.0


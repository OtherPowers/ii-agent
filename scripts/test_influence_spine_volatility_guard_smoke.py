"""
Smoke test: rapid posture changes must not amplify emission frequency.
The adapter may observe volatility, but emission must remain bounded.
"""

from unittest.mock import MagicMock

from otherpowers_governance.intelligence.influence_spine_adapter import (
    InfluenceSpineAdapter,
)


class _VolatileSpine:
    def __init__(self):
        self._states = ["open", "open", "open", "open"]

    def process(self, context):
        if not self._states:
            return None
        return {"posture": self._states.pop(0)}


class _RecordingBridge:
    def __init__(self):
        self.calls = 0

    def emit(self, summary):
        self.calls += 1
        return {"ok": True}


def test_volatility_does_not_amplify_emission():
    spine = _VolatileSpine()
    adapter = InfluenceSpineAdapter(spine=spine)

    bridge = _RecordingBridge()
    adapter._bridge = bridge

    # multiple rapid calls
    adapter.process({})
    adapter.process({})
    adapter.process({})
    adapter.process({})

    # emission must remain bounded (exact policy: 1 per batch)
    assert bridge.calls == 1


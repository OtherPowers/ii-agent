"""
Smoke test: InfluenceSpineAdapter emits exactly once
when the spine produces a value and governance allows it.
"""

from unittest.mock import MagicMock

from otherpowers_governance.intelligence.influence_spine_adapter import (
    InfluenceSpineAdapter,
)


class DummySpine:
    def process(self, context):
        return {"posture": "open"}


def test_positive_emission_calls_bridge_once():
    adapter = InfluenceSpineAdapter(spine=DummySpine())

    bridge = adapter._get_bridge()
    bridge.emit = MagicMock(return_value={"emitted": True})

    result = adapter.process(context={"anything": True})

    assert result == {"emitted": True}
    bridge.emit.assert_called_once()


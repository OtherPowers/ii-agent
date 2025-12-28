"""
Smoke test: when the spine produces a value but governance refuses emission,
InfluenceSpineAdapter must return None and must not emit.
"""

from unittest.mock import MagicMock

from otherpowers_governance.intelligence.influence_spine_adapter import (
    InfluenceSpineAdapter,
)


class DummySpine:
    def process(self, context):
        # Spine produces a value (non-silence)
        return {"posture": "open"}


def test_governance_refusal_returns_none_without_emission():
    adapter = InfluenceSpineAdapter(spine=DummySpine())

    # Lazily create the bridge and force governance refusal by making emit return None
    bridge = adapter._get_bridge()
    bridge.emit = MagicMock(return_value=None)

    result = adapter.process(context={"anything": True})

    assert result is None
    bridge.emit.assert_called_once()


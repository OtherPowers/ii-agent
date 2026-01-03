"""
Smoke test: callers must propagate None from InfluenceSpineAdapter
without attempting emission or mutation.
"""

from unittest.mock import MagicMock

from otherpowers_governance.intelligence.influence_spine_adapter import (
    InfluenceSpineAdapter,
)


def test_caller_propagates_none_without_emission():
    adapter = InfluenceSpineAdapter()

    # Guard: if anything tries to emit, this test must fail
    adapter._bridge.emit = MagicMock(side_effect=AssertionError("emit should not be called"))

    result = adapter.process(context={})

    assert result is None
    adapter._bridge.emit.assert_not_called()


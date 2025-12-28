"""
Smoke test: callers must propagate None from InfluenceSpineAdapter
without instantiating or invoking emission machinery.
"""

from otherpowers_governance.intelligence.influence_spine_adapter import (
    InfluenceSpineAdapter,
)


def test_caller_propagates_none_without_emission():
    adapter = InfluenceSpineAdapter()

    result = adapter.process(context={})

    assert result is None
    assert adapter._bridge is None

"""
Guard smoke test:
adapter must fail closed when spine is malformed.
"""

from otherpowers_governance.intelligence.influence_spine_adapter import (
    InfluenceSpineAdapter,
)


class _MalformedSpine:
    pass


def test_adapter_fails_closed_on_malformed_spine():
    adapter = InfluenceSpineAdapter(spine=_MalformedSpine())

    out = adapter.process({"anything": True})

    assert out is None


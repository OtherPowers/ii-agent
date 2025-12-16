import os
import tempfile

from otherpowers_governance.intelligence.influence_spine_adapter import (
    InfluenceSpineAdapter,
)


def test_influence_spine_smoke():
    adapter = InfluenceSpineAdapter()

    summary = {"pattern_families": ["care"]}

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        snapshot_path = tmp.name

    try:
        result = adapter.process(summary, snapshot_path=snapshot_path)
        assert result is not None
        assert os.path.exists(snapshot_path)
    finally:
        if os.path.exists(snapshot_path):
            os.remove(snapshot_path)


def test_influence_spine_allows_silence():
    adapter = InfluenceSpineAdapter()
    result = adapter.process({})
    assert result is None


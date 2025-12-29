from otherpowers_governance.intelligence.influence_spine_adapter import (
    InfluenceSpineAdapter,
)


class _Spine:
    def __init__(self, posture):
        self._posture = posture

    def process(self, context):
        return {"posture": self._posture}


class _NullStorage:
    def write(self, signal):
        return signal


def test_posture_is_accumulated_without_affecting_emission():
    adapter = InfluenceSpineAdapter(
        spine=_Spine("open"),
        cold_storage=_NullStorage(),
    )

    adapter.process({})
    adapter.process({})

    snap = adapter.posture_snapshot()
    assert snap.posture == "open"
    assert snap.weight == 2.0


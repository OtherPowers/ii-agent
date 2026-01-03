import pytest

from otherpowers_governance.signals.accumulator import GovernanceAccumulator


def test_ingest_ignores_silence():
    acc = GovernanceAccumulator(maxlen=4)
    acc.ingest(None)
    snap = acc.snapshot()
    assert snap.count == 0
    assert snap.last is None
    assert snap.history == []


def test_ingest_accepts_dict_and_does_not_mutate_input():
    acc = GovernanceAccumulator(maxlen=4)

    payload = {"a": 1, "b": {"nested": True}}
    acc.ingest(payload)

    # mutate caller-owned object after ingest
    payload["a"] = 999
    payload["b"]["nested"] = False

    snap = acc.snapshot()
    assert snap.count == 1
    assert snap.last == {"a": 1, "b": {"nested": True}}
    assert snap.history == [{"a": 1, "b": {"nested": True}}]


def test_retention_is_bounded_by_maxlen():
    acc = GovernanceAccumulator(maxlen=2)
    acc.ingest({"i": 1})
    acc.ingest({"i": 2})
    acc.ingest({"i": 3})

    snap = acc.snapshot()
    assert snap.count == 2
    assert snap.history == [{"i": 2}, {"i": 3}]
    assert snap.last == {"i": 3}


def test_snapshot_returns_new_object_each_call():
    acc = GovernanceAccumulator(maxlen=4)
    acc.ingest({"x": 1})

    s1 = acc.snapshot()
    s2 = acc.snapshot()

    assert s1 is not s2
    assert s1.history == s2.history
    assert s1.last == s2.last


def test_rejects_non_dict_emissions():
    acc = GovernanceAccumulator(maxlen=4)
    with pytest.raises(TypeError):
        acc.ingest("nope")


from otherpowers_governance.signals.posture_accumulator import (
    PostureAccumulator,
)


def test_posture_accumulates_and_decays():
    acc = PostureAccumulator()

    acc.update("open")
    acc.update("open")

    snap = acc.snapshot()
    assert snap.posture == "open"
    assert snap.weight == 2.0

    acc.update("guarded")

    snap = acc.snapshot()
    assert snap.posture == "guarded"
    assert snap.weight == 1.0


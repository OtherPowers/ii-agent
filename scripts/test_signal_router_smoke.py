from otherpowers_governance.signals.router import SignalRouter
from otherpowers_governance.signals.api import new_signal


def test_router_emits_once():
    r = SignalRouter()
    s = new_signal()

    assert r.route(s) == s
    assert r.route(s) is None


def test_router_respects_silence():
    r = SignalRouter()
    assert r.route({}) is None


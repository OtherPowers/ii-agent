import pytest

import otherpowers_governance.signals as signals


def test_only_new_signal_is_public():
    public = set(signals.__all__)

    assert public == {"new_signal"}


def test_schema_not_directly_accessible_from_package():
    with pytest.raises(AttributeError):
        _ = signals.Posture

    with pytest.raises(AttributeError):
        _ = signals.SignalEnvelope


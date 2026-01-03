from typing import Any, Dict, Optional

from otherpowers_governance.intelligence.influence_spine_adapter import InfluenceSpineAdapter
from otherpowers_governance.signals.schema import GovernanceDecision


class _BlockedProposal:
    def __init__(self) -> None:
        self.signal = {"kind": "test"}
        self.governance_decision = GovernanceDecision(allow=False)


class _SilentSpine:
    def propose(self, context: Dict[str, Any]) -> Optional[Any]:
        return None


class _BlockedSpine:
    def propose(self, context: Dict[str, Any]) -> Optional[Any]:
        return _BlockedProposal()


class _RecordingColdStorage:
    def __init__(self) -> None:
        self.stored = False

    def maybe_store(self, payload: Dict[str, Any]) -> None:
        self.stored = True


def test_adapter_returns_none_on_empty_context():
    adapter = InfluenceSpineAdapter(
        spine=_SilentSpine(),
        cold_storage=_RecordingColdStorage(),
    )

    out = adapter.process({})
    assert out is None


def test_adapter_returns_none_on_spine_silence():
    adapter = InfluenceSpineAdapter(
        spine=_SilentSpine(),
        cold_storage=_RecordingColdStorage(),
    )

    out = adapter.process({"some": "context"})
    assert out is None


def test_adapter_returns_none_on_governance_block():
    storage = _RecordingColdStorage()

    adapter = InfluenceSpineAdapter(
        spine=_BlockedSpine(),
        cold_storage=storage,
    )

    out = adapter.process({"some": "context"})

    assert out is None
    assert storage.stored is False

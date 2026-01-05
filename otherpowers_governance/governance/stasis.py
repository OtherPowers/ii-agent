from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from typing import Dict, Optional

from .renegotiation import RenegotiationIntent, RenegotiationResolution


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _fingerprint_dict(payload: dict) -> str:
    blob = repr(sorted(payload.items())).encode("utf-8")
    return sha256(blob).hexdigest()[:16]


def _intent_fingerprint(intent: Optional[RenegotiationIntent]) -> Optional[str]:
    if intent is None:
        return None
    payload = {
        "contested_invariant": intent.contested_invariant,
        "triggering_event": intent.triggering_event,
        "impacted_groups": tuple(intent.impacted_groups),
        "harm_claim": intent.harm_claim,
    }
    return _fingerprint_dict(payload)


class StasisActiveError(RuntimeError):
    pass


class InvalidResolutionError(ValueError):
    pass


class StasisEncountered(RuntimeError):
    def __init__(self, invariant: str, intent: Optional[RenegotiationIntent]):
        self.invariant = invariant
        self.intent = intent
        super().__init__(
            f"Stasis encountered on invariant: {invariant}\n"
            f"Resolution Context: intent_fp={_intent_fingerprint(intent)}"
        )


@dataclass
class _StasisSlot:
    invariant: str
    entered_at_utc: datetime
    expires_at_utc: Optional[datetime]
    intent: RenegotiationIntent


class StasisGate:
    def __init__(
        self,
        *,
        ttl: Optional[timedelta] = timedelta(hours=72),
        quorum_min: int = 2,
    ):
        self._ttl = ttl
        self._quorum_min = quorum_min
        self._slots: Dict[str, _StasisSlot] = {}

    def _expire_if_needed(self, invariant: str) -> None:
        slot = self._slots.get(invariant)
        if slot and slot.expires_at_utc and _now_utc() >= slot.expires_at_utc:
            self._slots.pop(invariant, None)

    def register_intent(self, intent: RenegotiationIntent) -> None:
        now = _now_utc()
        self._slots[intent.contested_invariant] = _StasisSlot(
            invariant=intent.contested_invariant,
            entered_at_utc=now,
            expires_at_utc=(now + self._ttl) if self._ttl else None,
            intent=intent,
        )

    def current_intent(self, invariant: str) -> Optional[RenegotiationIntent]:
        self._expire_if_needed(invariant)
        slot = self._slots.get(invariant)
        return slot.intent if slot else None

    def is_stasis_active(self, invariant: str) -> bool:
        return self.current_intent(invariant) is not None

    def require_not_in_stasis(self, invariant: str) -> None:
        if self.is_stasis_active(invariant):
            raise StasisActiveError(f"Stasis active for invariant: {invariant}")

    def apply_resolution(self, resolution: RenegotiationResolution) -> None:
        inv = resolution.contested_invariant
        intent = self.current_intent(inv)

        if intent is None:
            raise InvalidResolutionError("No active stasis for invariant")

        if not resolution.community_window_closed:
            raise InvalidResolutionError("Community window still open")

        if len(resolution.quorum_attestations) < self._quorum_min:
            raise InvalidResolutionError("Quorum not met")

        self._slots.pop(inv, None)


@dataclass(frozen=True)
class CollectiveTrace:
    contested_invariant: str
    origin: str
    detail_level: str


class RelationalThreshold:
    def __init__(
        self,
        gate: Optional[StasisGate] = None,
        *,
        decay_seconds: float = 0.0,
        retain_collective_trace: bool = False,
    ):
        self._gate = gate or StasisGate()
        self._decay_seconds = float(decay_seconds)
        self._retain_collective_trace = retain_collective_trace
        self._trace: Dict[str, CollectiveTrace] = {}

    def hold_space(self, intent: RenegotiationIntent) -> None:
        self._gate.register_intent(intent)

        if self._decay_seconds > 0:
            raise StasisEncountered(intent.contested_invariant, intent)

    def encounter(self, invariant: str) -> None:
        intent = self._gate.current_intent(invariant)
        if intent:
            raise StasisEncountered(invariant, intent)

    def stay_with_trouble(self, invariant: str) -> Optional[RenegotiationIntent]:
        return self._gate.current_intent(invariant)

    def acknowledge_resolution(self, resolution: RenegotiationResolution) -> None:
        inv = resolution.contested_invariant
        self._gate.apply_resolution(resolution)

        if self._retain_collective_trace:
            self._trace[inv] = CollectiveTrace(
                contested_invariant=inv,
                origin="stasis",
                detail_level="minimal",
            )

    def is_stasis_tended(self, invariant: str) -> bool:
        return self._gate.is_stasis_active(invariant)

    def collective_trace(self, invariant: str) -> Optional[CollectiveTrace]:
        return self._trace.get(invariant)


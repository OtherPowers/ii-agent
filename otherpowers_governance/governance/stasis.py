from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from typing import Dict, List, Optional, Sequence

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
        "contested_invariant": getattr(intent, "contested_invariant", None),
        "triggering_event": getattr(intent, "triggering_event", None),
        "impacted_groups": tuple(getattr(intent, "impacted_groups", []) or []),
        "harm_claim": getattr(intent, "harm_claim", None),
    }
    return _fingerprint_dict(payload)


def _resolution_fingerprint(resolution: RenegotiationResolution) -> str:
    payload = {
        "contested_invariant": getattr(resolution, "contested_invariant", None),
        "community_window_closed": getattr(resolution, "community_window_closed", None),
        "quorum_count": len(getattr(resolution, "quorum_attestations", []) or []),
        "summary": getattr(resolution, "summary", None),
    }
    return _fingerprint_dict(payload)


@dataclass(frozen=True)
class StasisRecord:
    invariant: str
    event: str
    at_utc: datetime
    intent_fp: Optional[str] = None
    resolution_fp: Optional[str] = None
    quorum_count: Optional[int] = None
    note: Optional[str] = None


class StasisActiveError(RuntimeError):
    pass


class StasisResolutionMismatch(ValueError):
    pass


class InvalidResolutionError(ValueError):
    pass


class StasisEncountered(RuntimeError):
    def __init__(self, invariant: str, intent: Optional[RenegotiationIntent] = None):
        self.invariant = invariant
        self.intent = intent
        super().__init__(self._format())

    def _format(self) -> str:
        if self.intent is None:
            return f"Stasis encountered on invariant: {self.invariant}\nResolution Context: (none)"
        return (
            f"Stasis encountered on invariant: {self.invariant}\n"
            f"Resolution Context: intent_fp={_intent_fingerprint(self.intent)}"
        )


@dataclass
class _StasisSlot:
    invariant: str
    entered_at_utc: datetime
    expires_at_utc: Optional[datetime]
    intent: Optional[RenegotiationIntent] = None


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
        self._history: Dict[str, List[StasisRecord]] = {}

    def _expire_if_needed(self, invariant: str) -> None:
        slot = self._slots.get(invariant)
        if not slot:
            return
        if slot.expires_at_utc and _now_utc() >= slot.expires_at_utc:
            self._slots.pop(invariant, None)
            self._history.setdefault(invariant, []).append(
                StasisRecord(
                    invariant=invariant,
                    event="expired",
                    at_utc=_now_utc(),
                    intent_fp=_intent_fingerprint(slot.intent),
                )
            )

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

    def clear_with_resolution(self, resolution: RenegotiationResolution) -> None:
        inv = resolution.contested_invariant
        intent = self.current_intent(inv)

        if intent is None:
            return

        if not resolution.community_window_closed:
            raise StasisActiveError("Community window still open")

        attestations = getattr(resolution, "quorum_attestations", []) or []
        if len(attestations) < self._quorum_min:
            raise InvalidResolutionError("Quorum not met")

        self._slots.pop(inv, None)


class RelationalThreshold:
    def __init__(self, gate: Optional[StasisGate] = None):
        self._gate = gate or StasisGate()

    def hold_space(self, intent: RenegotiationIntent) -> None:
        self._gate.register_intent(intent)

    def encounter(self, invariant: str) -> None:
        intent = self._gate.current_intent(invariant)
        if intent is not None:
            raise StasisEncountered(invariant, intent)

    def acknowledge_resolution(self, resolution: RenegotiationResolution) -> None:
        self._gate.clear_with_resolution(resolution)

    def is_stasis_tended(self, invariant: str) -> bool:
        return self._gate.current_intent(invariant) is not None


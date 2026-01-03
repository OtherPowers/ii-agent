from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from typing import Dict, List, Optional, Sequence

from .renegotiation import RenegotiationIntent, RenegotiationResolution


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _fingerprint_dict(payload: dict) -> str:
    # Stable, minimal fingerprint. No identities. No raw text dumps.
    blob = repr(sorted(payload.items())).encode("utf-8")
    return sha256(blob).hexdigest()[:16]


def _intent_fingerprint(intent: RenegotiationIntent) -> str:
    payload = {
        "contested_invariant": getattr(intent, "contested_invariant", None),
        "triggering_event": getattr(intent, "triggering_event", None),
        "impacted_groups": tuple(getattr(intent, "impacted_groups", []) or []),
        "harm_claim": getattr(intent, "harm_claim", None),
        "counter_harm_risk": getattr(intent, "counter_harm_risk", None),
        "non_negotiables": tuple(getattr(intent, "non_negotiables", []) or []),
        "alternatives_considered": tuple(getattr(intent, "alternatives_considered", []) or []),
        # Intentionally exclude submitted_by + any identity-ish fields.
    }
    return _fingerprint_dict(payload)


def _resolution_fingerprint(resolution: RenegotiationResolution) -> str:
    alt_trace = getattr(resolution, "alt_modality_trace", None)
    # alt_modality_trace may be list[str] or similar; we only store count + first short marker.
    alt_preview = None
    if isinstance(alt_trace, Sequence) and not isinstance(alt_trace, (str, bytes)):
        alt_preview = (alt_trace[0] if len(alt_trace) > 0 else None)
        alt_count = len(alt_trace)
    else:
        alt_preview = None
        alt_count = 0

    payload = {
        "contested_invariant": getattr(resolution, "contested_invariant", None),
        "community_window_closed": getattr(resolution, "community_window_closed", None),
        "quorum_count": len(getattr(resolution, "quorum_attestations", []) or []),
        "alt_count": alt_count,
        "alt_preview": alt_preview,
        "summary": getattr(resolution, "summary", None),
    }
    return _fingerprint_dict(payload)


@dataclass(frozen=True)
class StasisRecord:
    """
    Minimal, retroactively legible trace.
    - No identities.
    - No raw contextual dumps.
    - Just enough to reconstruct "what happened" later.
    """
    invariant: str
    event: str  # "entered" | "resolution_ack" | "expired" | "cleared"
    at_utc: datetime
    intent_fp: Optional[str] = None
    resolution_fp: Optional[str] = None
    quorum_count: Optional[int] = None
    note: Optional[str] = None


class StasisActiveError(RuntimeError):
    pass


class StasisResolutionMismatch(ValueError):
    pass


class StasisEncountered(RuntimeError):
    def __init__(self, contested_invariant: str, intent: Optional[RenegotiationIntent] = None):
        self.contested_invariant = contested_invariant
        self.intent = intent
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        # Tests expect "Resolution Context" to appear.
        base = f"Stasis encountered on invariant: {self.contested_invariant}"
        if self.intent is None:
            return f"{base}\nResolution Context: (none)"
        fp = _intent_fingerprint(self.intent)
        return f"{base}\nResolution Context: intent_fp={fp}"


@dataclass
class _StasisSlot:
    invariant: str
    entered_at_utc: datetime
    expires_at_utc: Optional[datetime]
    intent: Optional[RenegotiationIntent] = None
    last_resolution: Optional[RenegotiationResolution] = None


class StasisGate:
    """
    Non-bypassable stasis with temporal decay + minimal retroactive trace.
    """

    def __init__(
        self,
        *,
        ttl: Optional[timedelta] = timedelta(hours=72),
        history_limit_per_invariant: int = 64,
        quorum_min: int = 2,
    ):
        self._ttl = ttl
        self._history_limit = int(history_limit_per_invariant)
        self._quorum_min = int(quorum_min)

        self._slots: Dict[str, _StasisSlot] = {}
        self._history: Dict[str, List[StasisRecord]] = {}

    # --- history (retroactive trace) ---

    def history(self, invariant: str, *, limit: int = 20) -> List[StasisRecord]:
        items = self._history.get(invariant, [])
        if limit <= 0:
            return []
        return list(items[-limit:])

    def _append_history(self, record: StasisRecord) -> None:
        bucket = self._history.setdefault(record.invariant, [])
        bucket.append(record)
        if len(bucket) > self._history_limit:
            del bucket[: len(bucket) - self._history_limit]

    # --- temporal decay ---

    def _is_expired(self, slot: _StasisSlot, now: datetime) -> bool:
        return slot.expires_at_utc is not None and now >= slot.expires_at_utc

    def _expire_if_needed(self, invariant: str) -> None:
        slot = self._slots.get(invariant)
        if slot is None:
            return
        now = _now_utc()
        if not self._is_expired(slot, now):
            return

        # Expire stasis (decay), but keep trace.
        fp = _intent_fingerprint(slot.intent) if slot.intent is not None else None
        self._append_history(
            StasisRecord(
                invariant=invariant,
                event="expired",
                at_utc=now,
                intent_fp=fp,
                note="ttl_elapsed_unresolved",
            )
        )
        del self._slots[invariant]

    # --- stasis lifecycle ---

    def enter(self, contested_invariant: str) -> None:
        now = _now_utc()
        expires = (now + self._ttl) if self._ttl is not None else None
        slot = _StasisSlot(
            invariant=contested_invariant,
            entered_at_utc=now,
            expires_at_utc=expires,
            intent=None,
            last_resolution=None,
        )
        self._slots[contested_invariant] = slot
        self._append_history(
            StasisRecord(
                invariant=contested_invariant,
                event="entered",
                at_utc=now,
                note=("ttl_enabled" if expires is not None else "ttl_disabled"),
            )
        )

    def register_intent(self, intent: RenegotiationIntent) -> None:
        inv = intent.contested_invariant
        # Ensure slot exists.
        if inv not in self._slots:
            self.enter(inv)

        # Attach intent.
        slot = self._slots[inv]
        slot.intent = intent

        self._append_history(
            StasisRecord(
                invariant=inv,
                event="entered",
                at_utc=_now_utc(),
                intent_fp=_intent_fingerprint(intent),
                note="intent_registered",
            )
        )

    def current_intent(self, contested_invariant: str) -> Optional[RenegotiationIntent]:
        self._expire_if_needed(contested_invariant)
        slot = self._slots.get(contested_invariant)
        if slot is None:
            return None
        return slot.intent

    def is_active(self, contested_invariant: str) -> bool:
        self._expire_if_needed(contested_invariant)
        return contested_invariant in self._slots

    def ensure_permitted(self, contested_invariant: str) -> None:
        self._expire_if_needed(contested_invariant)
        if contested_invariant in self._slots:
            raise StasisActiveError(f"Stasis active for invariant: {contested_invariant}")

    def clear_with_resolution(self, resolution: RenegotiationResolution) -> None:
        inv = resolution.contested_invariant
        self._expire_if_needed(inv)

        slot = self._slots.get(inv)
        if slot is None:
            # Nothing to clear; still record for retroactive audit.
            self._append_history(
                StasisRecord(
                    invariant=inv,
                    event="resolution_ack",
                    at_utc=_now_utc(),
                    resolution_fp=_resolution_fingerprint(resolution),
                    quorum_count=len(getattr(resolution, "quorum_attestations", []) or []),
                    note="no_active_stasis",
                )
            )
            return

        if not getattr(resolution, "community_window_closed", False):
            raise StasisActiveError("Cannot clear stasis: community window still open")

        attest = getattr(resolution, "quorum_attestations", []) or []
        if len(attest) < self._quorum_min:
            raise StasisActiveError("Cannot clear stasis: quorum not met")

        slot.last_resolution = resolution

        self._append_history(
            StasisRecord(
                invariant=inv,
                event="resolution_ack",
                at_utc=_now_utc(),
                intent_fp=_intent_fingerprint(slot.intent) if slot.intent is not None else None,
                resolution_fp=_resolution_fingerprint(resolution),
                quorum_count=len(attest),
                note="quorum_met_window_closed",
            )
        )

        del self._slots[inv]

        self._append_history(
            StasisRecord(
                invariant=inv,
                event="cleared",
                at_utc=_now_utc(),
                resolution_fp=_resolution_fingerprint(resolution),
                quorum_count=len(attest),
            )
        )


class RelationalThreshold:
    """
    User-facing facade:
    - hold_space(intent) registers stasis without raising.
    - encounter(invariant) raises if stasis active + includes context string.
    - stay_with_trouble(invariant) returns the intent (if any).
    - acknowledge_resolution(resolution) clears stasis with quorum + window checks.
    - is_stasis_tended(invariant) tells if still active (decay-aware).
    - retroactive_trace(invariant) exposes minimal collective history.
    """

    def __init__(self, gate: Optional[StasisGate] = None):
        self._gate = gate or StasisGate()

    def hold_space(self, intent: RenegotiationIntent) -> None:
        self._gate.register_intent(intent)

    def encounter(self, contested_invariant: str) -> None:
        intent = self._gate.current_intent(contested_invariant)
        if intent is None:
            return
        raise StasisEncountered(contested_invariant, intent)

    def stay_with_trouble(self, contested_invariant: str) -> Optional[RenegotiationIntent]:
        return self._gate.current_intent(contested_invariant)

    def acknowledge_resolution(self, resolution: RenegotiationResolution) -> None:
        active_intent = self._gate.current_intent(resolution.contested_invariant)
        if active_intent is not None and active_intent.contested_invariant != resolution.contested_invariant:
            raise StasisResolutionMismatch("Resolution invariant mismatch")
        self._gate.clear_with_resolution(resolution)

    def is_stasis_tended(self, contested_invariant: str) -> bool:
        return self._gate.is_active(contested_invariant)

    def retroactive_trace(self, contested_invariant: str, *, limit: int = 20) -> List[StasisRecord]:
        return self._gate.history(contested_invariant, limit=limit)


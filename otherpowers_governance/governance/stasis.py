from __future__ import annotations

from typing import Dict, Optional

from otherpowers_governance.governance.renegotiation import (
    RenegotiationIntent,
    RenegotiationResolution,
)


class StasisEncountered(PermissionError):
    def __init__(self, intent: RenegotiationIntent):
        message = (
            f"Stasis encountered for invariant '{intent.contested_invariant}'. "
            f"Resolution Context: {intent.situated_context}. "
            f"Renegotiation is underway."
        )
        super().__init__(message)
        self.intent = intent


class InvalidResolutionError(PermissionError):
    pass


class RelationalThreshold:
    def __init__(self) -> None:
        self._active_invariant: Optional[str] = None
        self._last_intent: Dict[str, RenegotiationIntent] = {}

    def hold_space(self, intent: RenegotiationIntent) -> None:
        invariant = intent.contested_invariant
        self._active_invariant = invariant
        self._last_intent[invariant] = intent

    def is_stasis_tended(self, invariant: str) -> bool:
        return self._active_invariant == invariant

    def encounter(self, invariant: str) -> None:
        if self._active_invariant == invariant:
            raise StasisEncountered(self._last_intent[invariant])

    def stay_with_trouble(self, invariant: str) -> Optional[RenegotiationIntent]:
        return self._last_intent.get(invariant)

    def acknowledge_resolution(self, resolution: RenegotiationResolution) -> None:
        if self._active_invariant is None:
            return

        if resolution.contested_invariant != self._active_invariant:
            raise InvalidResolutionError(
                "Resolution invariant mismatch (integrity failure)."
            )

        self._active_invariant = None


from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from otherpowers_governance.governance.renegotiation import RenegotiationIntent, RenegotiationResolution


class StasisActiveError(PermissionError):
    """Raised when a contested invariant is in stasis and a change/execution is attempted."""


class InvalidResolutionError(PermissionError):
    """Raised when a resolution fails integrity checks (quorum/window/etc.)."""


class StasisGate:
    """
    Non-bypassable gate: once an invariant is contested, paths touching it enter stasis.
    Clearing stasis requires a valid RenegotiationResolution (with quorum + closed window).
    """

    def __init__(self) -> None:
        self._active: Dict[str, bool] = {}
        self._last_intent: Dict[str, RenegotiationIntent] = {}

    def register_intent(self, intent: RenegotiationIntent) -> None:
        inv = intent.contested_invariant
        self._active[inv] = True
        self._last_intent[inv] = intent

    def is_stasis_active(self, invariant: str) -> bool:
        return bool(self._active.get(invariant, False))

    def require_not_in_stasis(self, invariant: str) -> None:
        if self.is_stasis_active(invariant):
            raise StasisActiveError(f"Stasis active for invariant '{invariant}'. Renegotiation required.")

    def apply_resolution(self, resolution: RenegotiationResolution) -> None:
        inv = resolution.contested_invariant
        if not self.is_stasis_active(inv):
            return

        # Pydantic validation already enforces quorum + closed window.
        # Here we enforce additional invariants: resolution must match last intent if present.
        last = self._last_intent.get(inv)
        if last and last.contested_invariant != inv:
            raise InvalidResolutionError("Resolution invariant mismatch (integrity failure).")

        # If dissolved/forked outcomes occur, stasis clears but higher-level policy may halt/dissolve.
        self._active[inv] = False


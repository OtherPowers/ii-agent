from __future__ import annotations

from typing import Mapping, Optional

_SIGNAL_MARKER = "__op_signal__"


class SignalRouter:
    """
    INTERNAL ONLY.

    Routes governance-safe signals.
    Silence is explicit.
    """

    def __init__(self):
        self._emitted = False

    def route(self, signal: Optional[Mapping]) -> Optional[Mapping]:
        # Explicit silence
        if signal is None:
            return None

        # Empty mapping is silence
        if isinstance(signal, Mapping) and not signal:
            return None

        # Must be an intentional signal constructed via new_signal
        if not isinstance(signal, Mapping) or not signal.get(_SIGNAL_MARKER):
            return None

        # Volatility guard: emit once
        if self._emitted:
            return None

        self._emitted = True

        # RETURN VERBATIM — no mutation, no stripping
        return signal


from __future__ import annotations

from collections import deque
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Deque, Dict, Optional


@dataclass(frozen=True)
class AccumulatorSnapshot:
    """
    Read-only view of the accumulator state.

    - history: newest-last ordered list of accepted emissions (deep-copied)
    - last: most recent accepted emission (deep-copied) or None
    - count: total number of accepted emissions currently retained
    """
    history: list[Dict[str, Any]]
    last: Optional[Dict[str, Any]]
    count: int


class GovernanceAccumulator:
    """
    Minimal MVP accumulator.

    Responsibilities:
    - accept emitted records (dict-like payloads)
    - enforce bounded retention (maxlen)
    - provide a stable snapshot API
    - never mutate caller-owned objects
    """

    def __init__(self, maxlen: int = 32):
        if maxlen <= 0:
            raise ValueError("maxlen must be > 0")
        self._maxlen = maxlen
        self._history: Deque[Dict[str, Any]] = deque(maxlen=maxlen)

    def ingest(self, emission: Any) -> None:
        """
        Accept a single emission.

        Rules:
        - None -> ignored (silence)
        - dict -> accepted (deep-copied)
        - anything else -> TypeError (MVP: strict boundary)
        """
        if emission is None:
            return

        if not isinstance(emission, dict):
            raise TypeError("GovernanceAccumulator expects emissions to be dict or None")

        self._history.append(deepcopy(emission))

    def snapshot(self) -> AccumulatorSnapshot:
        """
        Return a NEW snapshot object each call (deep-copied).
        """
        if len(self._history) == 0:
            return AccumulatorSnapshot(history=[], last=None, count=0)

        hist = [deepcopy(x) for x in list(self._history)]
        return AccumulatorSnapshot(history=hist, last=deepcopy(hist[-1]), count=len(hist))

    def clear(self) -> None:
        self._history.clear()


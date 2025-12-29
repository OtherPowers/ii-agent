from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class PostureSnapshot:
    posture: str
    weight: float = 1.0


class PostureAccumulator:
    """
    Aggregates posture over time.

    This object does not emit signals.
    It does not enforce governance.
    It only remembers gently.
    """

    def __init__(self) -> None:
        self._current: Optional[PostureSnapshot] = None

    def update(self, posture: str, weight: float = 1.0) -> None:
        if self._current is None:
            self._current = PostureSnapshot(posture=posture, weight=weight)
            return

        if posture == self._current.posture:
            self._current.weight += weight
        else:
            # decay old posture instead of overwriting violently
            self._current.weight *= 0.5
            self._current = PostureSnapshot(posture=posture, weight=weight)

    def snapshot(self) -> Optional[PostureSnapshot]:
        return self._current

    def reset(self) -> None:
        self._current = None


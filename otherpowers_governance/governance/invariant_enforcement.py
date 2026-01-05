from typing import Iterable, Optional

from .stasis import StasisGate, StasisActiveError


class InvariantEnforcer:
    """
    Single, explicit enforcement surface.

    Any code path that intends to act must pass through this check.
    No implicit protection. No silent bypass.
    """

    def __init__(self, gate: StasisGate):
        self._gate = gate

    def require_clear(
        self,
        invariants: Iterable[str],
        *,
        context: Optional[str] = None,
    ) -> None:
        """
        Assert that all listed invariants are clear.

        Raises immediately on the first active stasis.
        """
        for invariant in invariants:
            self._gate.require_not_in_stasis(invariant)


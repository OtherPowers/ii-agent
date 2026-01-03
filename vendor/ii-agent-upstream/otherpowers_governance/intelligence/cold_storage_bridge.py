from __future__ import annotations

from typing import Any, Optional


class ColdStorageBridge:
    """
    Single responsibility:
    - accept a governance-approved signal
    - persist it (or refuse by returning None)

    This class must be boring, explicit, and side-effect constrained.
    """

    def __init__(self, cold_storage: Optional[Any] = None) -> None:
        self._cold_storage = cold_storage

    def emit(self, signal: dict) -> Optional[Any]:
        """
        Returns:
        - persisted signal (or downstream handle) on success
        - None if storage refuses or is unavailable
        """

        if self._cold_storage is None:
            return None

        if not hasattr(self._cold_storage, "write"):
            return None

        return self._cold_storage.write(signal)


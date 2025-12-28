from __future__ import annotations

from typing import Any, Optional, Callable


class InfluenceSpineAdapter:
    """
    Mediates between an influence spine and governance / cold storage.

    Accepts spines that are:
    - callable(context) -> Optional[signal]
    - or objects exposing .process(context)
    """

    def __init__(
        self,
        spine: Optional[Any] = None,
        cold_storage: Optional[Any] = None,
    ):
        self._spine = spine
        self._cold_storage = cold_storage
        self._bridge = None

    def _get_bridge(self):
        if self._bridge is None:
            if self._cold_storage is None:
                from otherpowers_governance.intelligence.cold_storage_bridge import (
                    ColdStoragePostureEmissionBridge,
                )

                self._bridge = ColdStoragePostureEmissionBridge()
            else:
                self._bridge = self._cold_storage

        return self._bridge

    def _invoke_spine(self, context: dict) -> Optional[Any]:
        """
        Invoke the spine in a shape-agnostic way.
        """

        spine = self._spine

        if spine is None:
            return None

        # Preferred: callable spine
        if callable(spine):
            return spine(context)

        # Fallback: object with process()
        process = getattr(spine, "process", None)
        if callable(process):
            return process(context)

        # Unknown spine shape → silence
        return None

    def process(self, context: dict) -> Optional[Any]:
        """
        Process context through the influence spine.

        Returns None when:
        - no spine
        - spine yields silence
        - governance refuses emission
        """

        result = self._invoke_spine(context)

        if result is None:
            return None

        bridge = self._get_bridge()
        emitted = bridge.emit(result)

        return emitted


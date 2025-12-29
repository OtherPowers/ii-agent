from __future__ import annotations

from typing import Any, Optional

from otherpowers_governance.signals.schema import PostureSnapshot


class InfluenceSpineAdapter:
    def __init__(
        self,
        spine: Optional[Any] = None,
        cold_storage: Optional[Any] = None,
    ):
        # ONLY reject raw objects with no interface
        if spine is not None:
            is_raw_object = type(spine) is object
            has_interface = callable(spine) or hasattr(spine, "process")

            if is_raw_object and not has_interface:
                raise TypeError(
                    "InfluenceSpineAdapter requires spine to be callable "
                    "or expose a .process(context) method"
                )

        self._spine = spine
        self._cold_storage = cold_storage

        self._posture: Optional[str] = None
        self._weight: float = 0.0
        self._emitted: bool = False

        self._bridge = None

    def process(self, context: Any) -> Optional[Any]:
        if self._spine is None:
            return None

        # Silent spines are allowed
        try:
            if callable(self._spine):
                result = self._spine(context)
            elif hasattr(self._spine, "process"):
                result = self._spine.process(context)
            else:
                return None
        except Exception:
            return None

        if result is None:
            return None

        if isinstance(result, dict):
            posture = result.get("posture")
            if posture is not None:
                if posture == self._posture:
                    self._weight += 1.0
                else:
                    self._posture = posture
                    self._weight = 1.0

        if self._emitted:
            return None

        bridge = self._get_bridge()
        emitted = bridge.emit(result)

        if emitted is None:
            return None

        self._emitted = True
        return emitted

    def posture_snapshot(self) -> PostureSnapshot:
        return PostureSnapshot(posture=self._posture, weight=self._weight)

    def _get_bridge(self):
        if self._bridge is not None:
            return self._bridge

        if self._cold_storage is None:
            self._bridge = _NullBridge()
        else:
            self._bridge = _ColdStorageBridge(self._cold_storage)

        return self._bridge


class _NullBridge:
    def emit(self, summary: Any) -> Optional[Any]:
        return summary


class _ColdStorageBridge:
    def __init__(self, storage: Any):
        self._storage = storage

    def emit(self, summary: Any) -> Optional[Any]:
        try:
            self._storage.record(summary)
        except Exception:
            return None
        return summary


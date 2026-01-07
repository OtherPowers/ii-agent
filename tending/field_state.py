from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional


def _coerce_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        # Treat naive as UTC, never local.
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _parse_fixed_time(value: str) -> datetime:
    # Expect ISO 8601. If parse fails, fall back safely.
    try:
        dt = datetime.fromisoformat(value)
        return _coerce_utc(dt)
    except Exception:
        return datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)


def _default_now_utc() -> datetime:
    # Deterministic by default (tests must not depend on wall clock).
    fixed = os.environ.get("OTHERPOWERS_FIXED_TIME")
    if fixed:
        return _parse_fixed_time(fixed)
    return datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)


def _season_for_month(month: int) -> str:
    # Simple, stable, non-analytic mapping (northern hemisphere).
    if month in (12, 1, 2):
        return "winter"
    if month in (3, 4, 5):
        return "spring"
    if month in (6, 7, 8):
        return "summer"
    return "autumn"


def _diurnal_for_hour(hour: int) -> str:
    # Minimal: day/night only.
    return "day" if 6 <= hour < 18 else "night"


@dataclass(frozen=True)
class FieldState:
    """
    ABI-stable FieldState compatibility contract.

    - accepts timestamp_utc= and legacy timestamp=
    - exposes both attributes
    - enforces UTC
    - carries minimal sensed attributes used by the surface + lattice
    """

    timestamp_utc: datetime
    seasons: List[str]
    diurnal_phase: str
    expressive_density: float

    def __init__(
        self,
        timestamp_utc: Optional[datetime] = None,
        *,
        timestamp: Optional[datetime] = None,
        seasons: Optional[List[str]] = None,
        diurnal_phase: Optional[str] = None,
        expressive_density: Optional[float] = None,
    ):
        if timestamp_utc is None:
            timestamp_utc = timestamp if timestamp is not None else _default_now_utc()
        ts = _coerce_utc(timestamp_utc)

        if seasons is None:
            seasons = [_season_for_month(ts.month)]
        else:
            seasons = list(seasons)

        if diurnal_phase is None:
            diurnal_phase = _diurnal_for_hour(ts.hour)

        if expressive_density is None:
            expressive_density = 0.5

        object.__setattr__(self, "timestamp_utc", ts)
        object.__setattr__(self, "seasons", seasons)
        object.__setattr__(self, "diurnal_phase", diurnal_phase)
        object.__setattr__(self, "expressive_density", float(expressive_density))

    @property
    def timestamp(self) -> datetime:
        # Legacy alias (read-only).
        return self.timestamp_utc

    @classmethod
    def sense(cls) -> "FieldState":
        ts = _default_now_utc()
        return cls(
            timestamp_utc=ts,
            seasons=[_season_for_month(ts.month)],
            diurnal_phase=_diurnal_for_hour(ts.hour),
            expressive_density=0.5,
        )


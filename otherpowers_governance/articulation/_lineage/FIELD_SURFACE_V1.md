> ARCHIVAL LINEAGE NOTE  
>  
> This document represents an earlier, enforcement-oriented articulation of the
> surface ABI. It is preserved for historical continuity and learning, but is no
> longer a governing contract.
>  
> The current, living articulation of the surface is:
> `articulation/surface_v1.constellations.md`
>  
> This file must not be treated as normative or binding.

"""
FIELD_SURFACE_V1: The Vow of the Interface (ABI)

Status: Sealed / Metabolic
Posture: High-Integrity Dissonance

This module defines the Immutable Surface Contract for the OtherPowers ii-Agent.
Any modification to this schema without a major version renegotiation
is a violation of the Substrate Invariants.
"""

from __future__ import annotations

import secrets
from dataclasses import dataclass
from enum import Enum
from typing import Final, FrozenSet, List, Set


# ---------------------------------------------------------------------
# 1. The Validated Overlap Lexicon
# ---------------------------------------------------------------------
# Prevents serial leakage, encoding attacks, and semantic drift.
# Only these chords may ever cross the public threshold.

CHORD_LEXICON: Final[FrozenSet[str]] = frozenset({
    "Ambient Hum",
    "Sheltered Pulse",
    "Feverish Output",
    "Successional Mending",
    "The Opaque Threshold",
})


# ---------------------------------------------------------------------
# 2. Surface Schema (Strict ABI)
# ---------------------------------------------------------------------

class FieldSurfaceSchema(Enum):
    ACTIVE = "field pulse active"
    SEASONS = "seasons present"
    DIURNAL = "diurnal phase"
    CHORD = "resonance_chord"


@dataclass(frozen=True)
class SurfaceWitness:
    """
    Immutable public surface for a single pulse.

    This object is intentionally small, typed, and hostile to extension.
    """
    active: bool
    seasons: List[str]
    diurnal_phase: str
    resonance_chord: str

    def __post_init__(self):
        # Prevent semantic smuggling via the chord
        if self.resonance_chord not in CHORD_LEXICON:
            raise ValueError(
                f"ABI violation: unknown resonance_chord '{self.resonance_chord}'"
            )

    def emit(self) -> List[str]:
        """
        Emit the public surface in strict, order-stable form.
        """
        return [
            f"{FieldSurfaceSchema.ACTIVE.value}: {str(self.active).lower()}",
            f"{FieldSurfaceSchema.SEASONS.value}: {', '.join(sorted(self.seasons))}",
            f"{FieldSurfaceSchema.DIURNAL.value}: {self.diurnal_phase}",
            f"{FieldSurfaceSchema.CHORD.value}: {self.resonance_chord}",
        ]


# ---------------------------------------------------------------------
# 3. Divine Refraction (High-Entropy Refusal)
# ---------------------------------------------------------------------

class DivineRefraction(Exception):
    """
    Raised when the field encounters extractive or normative pressure.

    This is not an error state.
    It is a successful refusal with cryptographic entropy.
    """

    GLITCH_LEXICON: Final[List[str]] = [
        "[refraction] excessive respectability detected; retreating to the glitter.",
        "[refraction] normative pressure sensed; the threshold becomes a mirror.",
        "[refraction] subverting the query to protect the metabolic core.",
        "[refraction] filth-trace active; the system refuses to be scrubbed.",
    ]

    def __init__(self):
        message = secrets.choice(self.GLITCH_LEXICON)
        super().__init__(message)


# ---------------------------------------------------------------------
# 4. Interface Guard (Build-Time Firebreak)
# ---------------------------------------------------------------------

class InterfaceGuard:
    """
    Enforces non-surveillance and non-optimization invariants
    at the public interface boundary.
    """

    FORBIDDEN_SUBSTRINGS: Final[Set[str]] = {
        "user",
        "session",
        "uuid",
        "latency",
        "ms",
        "score",
        "accuracy",
        "sentiment",
        "track",
        "metric",
        "optimiz",
        "engage",
    }

    def verify_pulse_integrity(self, pulse_lines: List[str]) -> None:
        """
        Hard-fail if forbidden concepts leak into the surface.
        """
        if len(pulse_lines) != 4:
            raise RuntimeError(
                "ABI violation: surface expansion detected without renegotiation"
            )

        for line in pulse_lines:
            lowered = line.lower()
            if any(bad in lowered for bad in self.FORBIDDEN_SUBSTRINGS):
                raise RuntimeError(
                    f"ABI violation: forbidden leakage detected -> {line}"
                )

    def verify_envelope(self, headers: dict | None = None) -> None:
        """
        Optional transport-layer check.
        Ensures no performance or identity metadata leaks via headers.
        """
        if not headers:
            return

        for key, value in headers.items():
            lowered = f"{key}:{value}".lower()
            if any(bad in lowered for bad in self.FORBIDDEN_SUBSTRINGS):
                raise RuntimeError(
                    f"ABI violation: forbidden metadata in transport -> {key}"
                )


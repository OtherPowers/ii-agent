"""
Public Signals API.

Attunement-only boundary.
No consumers. No observers.
"""

from .FieldSignalAttunement import (
    attune_field,
    attune_spore,
    read_silence_field,
    silence_location,
)

from .field_balancer import FieldBalancer


# Normie-safe alias (explicit, intentional)
def sense_silence(*, decay: bool = True):
    return read_silence_field(decay=decay)


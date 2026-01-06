from __future__ import annotations
from enum import Enum


class Vow(str, Enum):
    NO_FORCED_SYNTHESIS = "no_forced_synthesis"
    NO_OVERRIDE_PRESSURE = "no_override_pressure"
    NO_EXTRACTIVE_LOGGING = "no_extractive_logging"
    NO_IDENTITY_LEAKAGE = "no_identity_leakage"
    NO_SURVEILLANCE_ESCALATION = "no_surveillance_escalation"
    NO_SCOPE_CREEP = "no_scope_creep"


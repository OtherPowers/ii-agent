import os
from typing import Any, Dict, Optional

from otherpowers_governance.signals.posture_field_state import read_field_state
from otherpowers_governance.signals.silence_field import read_silence_field, silence_field_path


ENV_POSTURE_FIELD_STATE = "OTHERPOWERS_POSTURE_FIELD_STATE"
ENV_SPORE_FIELD_STATE = "OTHERPOWERS_SPORE_FIELD_STATE"

DEFAULT_POSTURE_FIELD_STATE = "/tmp/otherpowers_posture.field_state"
DEFAULT_SPORE_FIELD_STATE = "/tmp/otherpowers_spore.field_state"


def _resolve(path: Optional[str], env_key: str, default: str) -> str:
    return path or os.environ.get(env_key) or default


def attune_posture_field(path: Optional[str] = None) -> Dict[str, Any]:
    p = _resolve(path, ENV_POSTURE_FIELD_STATE, DEFAULT_POSTURE_FIELD_STATE)
    data = dict(read_field_state(p))
    return {
        "posture": data.get("posture"),
        "confidence": data.get("confidence"),
        "reason": data.get("reason"),
        "field": data.get("field"),
    }


def attune_otherpowers_field(path: Optional[str] = None) -> Dict[str, Any]:
    p = _resolve(path, ENV_SPORE_FIELD_STATE, DEFAULT_SPORE_FIELD_STATE)
    return dict(read_field_state(p))


def sense_silence(*, decay: bool = True) -> Dict[str, Any]:
    return dict(read_silence_field(decay=decay))


def silence_field_location() -> str:
    return silence_field_path()


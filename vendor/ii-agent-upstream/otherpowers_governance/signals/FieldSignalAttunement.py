import os
from typing import Any, Dict, Optional

from field_attunement.field import read_field
from field_attunement.spore import read_spore
from field_attunement.silence import read_silence, silence_path


ENV_FIELD_PATH = "OTHERPOWERS_FIELD_PATH"
ENV_SPORE_PATH = "OTHERPOWERS_SPORE_PATH"


def _resolve(path: Optional[str], env_key: str) -> Optional[str]:
    return path or os.environ.get(env_key)


def attune_field(path: Optional[str] = None) -> Dict[str, Any]:
    p = _resolve(path, ENV_FIELD_PATH)
    return read_field(p)


def attune_spore(path: Optional[str] = None) -> Dict[str, Any]:
    p = _resolve(path, ENV_SPORE_PATH)
    return read_spore(p)


def read_silence_field(*, decay: bool = True) -> Dict[str, Any]:
    return read_silence(decay=decay)


def silence_location() -> str:
    return silence_path()


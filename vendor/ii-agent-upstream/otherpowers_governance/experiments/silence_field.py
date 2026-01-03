import json
import os
from typing import Dict, Optional

SILENCE_FIELD_PATH = "/tmp/otherpowers_silence.field"


def _load() -> Dict[str, object]:
    if not os.path.exists(SILENCE_FIELD_PATH):
        return {}
    try:
        with open(SILENCE_FIELD_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def _save(field: Dict[str, object]):
    with open(SILENCE_FIELD_PATH, "w") as f:
        json.dump(field, f)


def register_silence(traits: Dict[str, Dict[str, str]]):
    """
    Records multi-dimensional silence with counterfactuals.
    No timestamps. No identities. Local-only.
    """
    field = _load()

    silence = field.get("silence", {})
    silence["frequency"] = int(silence.get("frequency", 0)) + 1
    silence["dimensions"] = traits

    field["silence"] = silence
    _save(field)


def read_silence_field(*, decay: bool = True) -> Dict[str, object]:
    """
    Reads the silence field. If decay=True, composts silence frequency by 1 per read
    (down to 0). No clocks, no timestamps, no attribution.
    """
    field = _load()
    silence = field.get("silence")
    if not isinstance(silence, dict):
        return field

    if decay:
        freq = int(silence.get("frequency", 0))
        if freq > 0:
            silence["frequency"] = freq - 1
            silence["composted"] = True
            field["silence"] = silence
            _save(field)

    return field


def clear_silence_field():
    try:
        os.remove(SILENCE_FIELD_PATH)
    except FileNotFoundError:
        pass


def silence_field_path() -> str:
    return SILENCE_FIELD_PATH


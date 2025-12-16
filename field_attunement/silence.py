import json
import os
from typing import Dict, Any

SILENCE_PATH = "/tmp/otherpowers_silence.json"


def _load() -> Dict[str, Any]:
    if not os.path.exists(SILENCE_PATH):
        return {}
    try:
        with open(SILENCE_PATH, "r") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _save(data: Dict[str, Any]) -> None:
    try:
        with open(SILENCE_PATH, "w") as f:
            json.dump(data, f)
    except Exception:
        pass


def read_silence(*, decay: bool = True) -> Dict[str, Any]:
    field = _load()
    silence = field.get("silence", {})

    freq = int(silence.get("frequency", 0))
    if decay:
        freq = max(0, freq - 1)

    silence["frequency"] = freq
    field["silence"] = silence
    _save(field)

    return field


def silence_path() -> str:
    return SILENCE_PATH


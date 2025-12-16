import json
import os
from typing import Dict, Any, Optional

DEFAULT_FIELD_PATH = "/tmp/otherpowers_field.json"


def read_field(path: Optional[str] = None) -> Dict[str, Any]:
    p = path or DEFAULT_FIELD_PATH
    if not os.path.exists(p):
        return {}
    try:
        with open(p, "r") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def write_field(data: Dict[str, Any], path: Optional[str] = None) -> None:
    p = path or DEFAULT_FIELD_PATH
    tmp = f"{p}.tmp"
    try:
        with open(tmp, "w") as f:
            json.dump(data if isinstance(data, dict) else {}, f)
        os.replace(tmp, p)
    except Exception:
        pass


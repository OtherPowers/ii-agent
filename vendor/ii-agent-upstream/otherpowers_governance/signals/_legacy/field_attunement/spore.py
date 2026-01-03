cat > /Users/bush3000/ii-agent-reorg/field_attunement/spore.py << 'EOF'
import os
import json
from typing import Dict, Any, Optional

ENV_SPORE_PATH = "OTHERPOWERS_SPORE_PATH"
DEFAULT_SPORE_PATH = "/tmp/otherpowers_spore.field"


def _resolve(path: Optional[str] = None) -> str:
    return path or os.environ.get(ENV_SPORE_PATH) or DEFAULT_SPORE_PATH


def read_spore(path: Optional[str] = None) -> Dict[str, Any]:
    p = _resolve(path)
    if not os.path.exists(p):
        return {}
    try:
        with open(p, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def write_spore(data: Dict[str, Any], path: Optional[str] = None) -> None:
    p = _resolve(path)
    tmp = f"{p}.tmp"
    with open(tmp, "w") as f:
        json.dump(data, f)
    os.replace(tmp, p)
EOF

from typing import Dict, Any, Optional, Literal

Posture = Literal[
    "open",
    "contained",
    "tender",
    "resting",
    "flux",
]


def reflect_posture(field: Dict[str, Any]) -> Optional[Posture]:
    posture = field.get("posture")
    if posture in (
        "open",
        "contained",
        "tender",
        "resting",
        "flux",
    ):
        return posture
    return None


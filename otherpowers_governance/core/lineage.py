"""
Optional reflective lineage context.

Never imported automatically.
Never required.
Never used for gating or enforcement.
"""

from typing import Dict, List
from ..inspiration_registry import INSPIRATION_WIKIPEDIA


LINEAGE_THEMES: Dict[str, List[str]] = {
    "care": ["Alice Wong", "adrienne maree brown"],
    "plurality": ["Ursula K. Le Guin", "Donna Haraway"],
    "abolition": ["Assata Shakur", "James Baldwin"],
    "creative_emergence": ["Octavia E. Butler", "Claude Cahun"],
}


def get_lineage(theme: str) -> Dict[str, str]:
    names = LINEAGE_THEMES.get(theme, [])
    return {
        name: INSPIRATION_WIKIPEDIA[name]
        for name in names
        if name in INSPIRATION_WIKIPEDIA
    }

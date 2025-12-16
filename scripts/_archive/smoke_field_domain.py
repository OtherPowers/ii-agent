"""
Smoke test for field_attunement domain.

Run:
python3 /Users/bush3000/ii-agent-reorg/scripts/smoke_field_domain.py
"""

import sys
from pathlib import Path

# ensure repo root is on path
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from field_attunement.field import write_field, read_field
from field_attunement.posture import reflect_posture
from field_attunement.silence import register_silence, read_silence, clear_silence
from field_attunement.spore import write_spore, read_spore
from field_attunement.impression import FieldImpression


def main():
    clear_silence()

    write_field({
        "posture": "open",
        "axes": {
            "care": 0.8,
            "volatility": 0.1,
            "erasure": 0.0,
        }
    })

    field = read_field()
    print("field:", field)

    posture = reflect_posture(field)
    print("posture:", posture)

    register_silence({
        "overwhelm": {
            "signal": "high input density",
            "counterfactual": "pause allowed"
        }
    })

    silence = read_silence()
    print("silence:", silence)

    write_spore({
        "hint": "gentle presence",
        "posture": posture
    })

    spore = read_spore()
    print("spore:", spore)

    impression = FieldImpression().impression({
        **field,
        **silence,
    })
    print("impression:", impression)

    print("\nSMOKE TEST: OK")


if __name__ == "__main__":
    main()


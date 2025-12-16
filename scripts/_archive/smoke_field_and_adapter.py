"""
Smoke test: field_attunement + governance adapter boundary

Run:
python3 /Users/bush3000/ii-agent-reorg/scripts/smoke_field_and_adapter.py
"""

import sys
from pathlib import Path

# ensure repo root on path
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from field_attunement.field import write_field, read_field
from field_attunement.silence import register_silence, read_silence, clear_silence
from field_attunement.spore import write_spore, read_spore
from field_attunement.impression import FieldImpression

from otherpowers_governance.signals.FieldSignalListener import (
    attune_field,
    attune_spore,
    sense_silence,
    silence_location,
)


def main():
    clear_silence()

    write_field({
        "posture": "open",
        "axes": {
            "care": 0.6,
            "volatility": 0.2,
            "erasure": 0.0,
        }
    })

    field_direct = read_field()
    print("direct field:", field_direct)

    field_adapter = attune_field()
    print("adapter field:", field_adapter)

    register_silence({
        "pause": {
            "signal": "dense input",
            "counterfactual": "rest permitted"
        }
    })

    silence_direct = read_silence()
    silence_adapter = sense_silence()
    print("direct silence:", silence_direct)
    print("adapter silence:", silence_adapter)
    print("silence path:", silence_location())

    write_spore({
        "hint": "ambient care",
        "posture": field_direct.get("posture")
    })

    spore_direct = read_spore()
    spore_adapter = attune_spore()
    print("direct spore:", spore_direct)
    print("adapter spore:", spore_adapter)

    impression = FieldImpression().impression({
        **field_direct,
        **silence_direct,
    })
    print("impression:", impression)

    print("\nSMOKE TEST: OK")


if __name__ == "__main__":
    main()


import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from otherpowers_governance.signals.api import (
    attune_field,
    attune_spore,
    sense_silence,
    FieldBalancer,
)

def main():
    print("field via api:", attune_field())
    print("spore via api:", attune_spore())
    print("silence via api:", sense_silence())

    balancer = FieldBalancer()
    out = balancer.balance({"axes": {"care": 0.5}, "confidence": "medium"})
    print("balancer:", out)

    print("\nAPI SMOKE: OK")

if __name__ == "__main__":
    main()


"""
Local canary for OtherPowers ii-agent.

Purpose:
- Prove ergonomics
- Catch regressions
- Exercise empty / silent paths
"""

from otherpowers_governance import (
    attune_field,
    sense_silence,
    FieldBalancer,
)


def main():
    field = attune_field()          # may be {}
    silence = sense_silence()       # may be {}

    balancer = FieldBalancer()
    result = balancer.balance({
        "axes": {"care": 0.2},
        "confidence": "soft",
    })

    print("FIELD:", field)
    print("SILENCE:", silence)
    print("POSTURE:", result)


if __name__ == "__main__":
    main()


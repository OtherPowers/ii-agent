"""
Test: PostureAccumulator hysteresis prevents rapid downshift

Run:
  cd /Users/bush3000/ii-agent-reorg
  PYTHONPATH=/Users/bush3000/ii-agent-reorg python3 scripts/test_posture_accumulator_hysteresis.py
"""

import time

from otherpowers_governance.signals import (
    OtherPowers_GovernanceSignal,
    OtherPowers_PostureAccumulator,
)


def main():
    acc = OtherPowers_PostureAccumulator(
        agent_salt="test_agent_hys",
        rules={
            "half_life_seconds": 60 * 60,
            "min_hold_seconds": 5,
            "downshift_penalty": 0.20,
        },
    )

    # Push up to high_caution
    sig1 = OtherPowers_GovernanceSignal(posture="high_caution", source="hys_test")
    acc.ingest(sig1.as_dict())
    r1 = acc.current_recommendation()
    print("\n[UPSHIFT]")
    print(r1)
    assert r1["posture"] in ("increase_caution", "high_caution", "freeze")

    # Immediately push "normal" and verify we do not instantly downshift
    sig2 = OtherPowers_GovernanceSignal(posture="normal", source="hys_test")
    acc.ingest(sig2.as_dict())
    r2 = acc.current_recommendation()
    print("\n[IMMEDIATE DOWNSHIFT ATTEMPT]")
    print(r2)
    assert r2["posture"] == r1["posture"]

    # After hold time, downshift may be allowed depending on weights
    time.sleep(6)
    r3 = acc.current_recommendation()
    print("\n[AFTER HOLD WINDOW]")
    print(r3)

    print("\n[PASS] Hysteresis behaves as expected.")


if __name__ == "__main__":
    main()


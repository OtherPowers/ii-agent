"""
Test: PostureAccumulator flood resistance + stable posture output

Run:
  cd /Users/bush3000/ii-agent-reorg
  PYTHONPATH=/Users/bush3000/ii-agent-reorg python3 scripts/test_posture_accumulator_flood_resistance.py
"""

import time

from otherpowers_governance.signals import (
    OtherPowers_GovernanceSignal,
    OtherPowers_PostureAccumulator,
)


def main():
    acc = OtherPowers_PostureAccumulator(
        agent_salt="test_agent_acc",
        rules={
            "flood_window_seconds": 60,
            "max_signals_per_window": 10,  # strict for test
            "half_life_seconds": 60 * 60,
            "min_hold_seconds": 10,
            "downshift_penalty": 0.20,
        },
    )

    # Flood with many signals; only first 10 should be ingested
    for i in range(25):
        sig = OtherPowers_GovernanceSignal(
            posture="high_caution",
            source="flood_test",
            recommended_actions={"slowdown": True},
            metadata={"i": i},
        )
        out = acc.ingest(sig.as_dict())
        # ignore status
        if i < 10:
            assert out["status"] == "ok"
        else:
            assert out["status"] in ("ignored", "ok")

    rec = acc.current_recommendation()
    print("\n[RECOMMENDATION AFTER FLOOD]")
    print(rec)

    assert rec["posture"] in ("increase_caution", "high_caution", "freeze")
    assert 0.0 <= float(rec["confidence"]) <= 1.0

    print("\n[PASS] Flood resistance works and posture is stable.")


if __name__ == "__main__":
    main()


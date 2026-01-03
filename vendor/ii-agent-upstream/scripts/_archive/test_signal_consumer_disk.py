"""
Test: GovernanceSignalConsumer (disk artifact)

Run:
  cd /Users/bush3000/ii-agent-reorg
  PYTHONPATH=/Users/bush3000/ii-agent-reorg python3 scripts/test_signal_consumer_disk.py
"""

import os

from otherpowers_governance.signals import OtherPowers_GovernanceSignal, OtherPowers_GovernanceSignalConsumer


ARTIFACT_PATH = "audit_logs/signals/_TEST_governance_signal.json"


def _rm(path: str) -> None:
    try:
        if os.path.isfile(path):
            os.remove(path)
    except Exception:
        pass


def main():
    _rm(ARTIFACT_PATH)

    sig = OtherPowers_GovernanceSignal(
        posture="high_caution",
        source="unit_test_disk",
        recommended_actions={"slowdown": True, "local_only": True},
        metadata={"note": "disk_test"},
    )
    sig.emit_json_artifact(path=ARTIFACT_PATH)

    consumer = OtherPowers_GovernanceSignalConsumer(agent_salt="test_agent_B")
    out = consumer.consume_artifact(ARTIFACT_PATH)

    print("\n[DISK CONSUME]")
    print(out)

    assert out["status"] == "ok"
    assert out["posture"] == "high_caution"
    assert out["non_coercive"] is True

    print("\n[PASS] Disk consumer works.")


if __name__ == "__main__":
    main()


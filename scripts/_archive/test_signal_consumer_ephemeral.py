"""
Test: GovernanceSignalConsumer (ephemeral / in-memory)

Run:
  cd /Users/bush3000/ii-agent-reorg
  PYTHONPATH=/Users/bush3000/ii-agent-reorg python3 scripts/test_signal_consumer_ephemeral.py
"""

from otherpowers_governance.signals import OtherPowers_GovernanceSignal, OtherPowers_GovernanceSignalConsumer


def main():
    sig = OtherPowers_GovernanceSignal(
        posture="increase_caution",
        source="unit_test",
        recommended_actions={"slowdown": True, "require_human_review": True},
        metadata={"note": "test"},
    )

    consumer = OtherPowers_GovernanceSignalConsumer(agent_salt="test_agent_A")

    out = consumer.consume_record(sig.as_dict())
    print("\n[EPHEMERAL CONSUME]")
    print(out)

    assert out["status"] == "ok"
    assert out["non_coercive"] is True
    assert out["posture"] == "increase_caution"
    assert 0.0 <= float(out["influence_probability"]) <= 1.0
    assert "suggested_actions" in out

    print("\n[PASS] Ephemeral consumer works.")


if __name__ == "__main__":
    main()


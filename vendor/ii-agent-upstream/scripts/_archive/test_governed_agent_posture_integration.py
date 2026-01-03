"""
Test: Governed agent posture-aware execution

Run:
  cd /Users/bush3000/ii-agent-reorg
  PYTHONPATH=/Users/bush3000/ii-agent-reorg python3 scripts/test_governed_agent_posture_integration.py
"""

from agents.otherpowers_governed_agent import OtherPowers_GovernedAgent
from otherpowers_governance.signals import OtherPowers_GovernanceSignal


def main():
    agent = OtherPowers_GovernedAgent(agent_id="agent_posture_test")

    # Inject a governance signal
    sig = OtherPowers_GovernanceSignal(
        posture="high_caution",
        source="integration_test",
        recommended_actions={"slowdown": True},
    )
    agent.observe_governance_signal(sig.as_dict())

    # Execute a benign intent
    intent = {
        "intent_id": "intent_123",
        "action": "process_data",
    }

    out = agent.execute_intent(intent=intent)
    print("\n[EXECUTION OUTPUT]")
    print(out)

    assert out["status"] == "executed"
    assert out["execution_hints"]["posture"] == "high_caution"
    assert out["execution_hints"]["suggest_human_review"] is True

    print("\n[PASS] Governed agent respects posture without coercion.")


if __name__ == "__main__":
    main()


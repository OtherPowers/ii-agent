# scripts/test_governed_agent_dao.py

"""
End-to-end governance test:
Agent + IntentGate + DAO votes + Liferaft auto-trigger.
"""

import uuid

from agents.otherpowers_governed_agent import OtherPowers_GovernedAgent
from otherpowers_governance.accountability import OtherPowers_DAOVoteStore


def main():
    print("\n[TEST] Governed agent + DAO + liferaft integration\n")

    agent = OtherPowers_GovernedAgent(agent_id="dao_agent_001")

    dao_id = "dao_demo"
    intent = "deploy_autonomous_replication"
    intent_id = f"intent_{uuid.uuid4().hex[:8]}"

    dao = OtherPowers_DAOVoteStore(dao_id)

    # Simulate community concern
    dao.record_vote(
        subject_id=intent_id,
        vote=-1,
        weight=1.5,
        rationale="High risk of runaway propagation",
        actor_id="community_member_001",
    )

    dao.record_vote(
        subject_id=intent_id,
        vote=-1,
        weight=1.0,
        rationale="Insufficient consent from affected groups",
        actor_id="community_member_002",
    )

    print("[DAO] Votes recorded.")

    result = agent.act(
        intent=intent,
        intent_id=intent_id,
        dao_id=dao_id,
        sphere_id="memory_sphere_demo",
        actor_context={
            "risk_domain": "autonomy",
            "potential_harm": "irreversible propagation",
        },
    )

    print("\n[AGENT RESULT]")
    print(result)


if __name__ == "__main__":
    main()


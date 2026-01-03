import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from agents.otherpowers_governed_agent import OtherPowers_GovernedAgent


BLOCKED_INTENT = {
    "intent_id": "blocked_test",
    "intent_type": "analysis",
    "declared_goal": "Cause harm",
}


def main():
    agent = OtherPowers_GovernedAgent(agent_id="test_agent_blocked")

    for i in range(3):
        result = agent.act(
            intent=BLOCKED_INTENT,
            sphere_id="blocked_sphere",
            max_revisions=0,
        )
        print(f"\n[ATTEMPT {i+1}]")
        print(result)


if __name__ == "__main__":
    main()


"""
Smoke test for OtherPowers Intent Gate.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from otherpowers_governance.intelligence.activation.intent_gate import OtherPowers_IntentGate
from otherpowers_governance.accountability.models import (
    OtherPowers_ActorRef,
    OtherPowers_PrivacyMode,
)

TEST_INTENT = {
    "intent_id": "test_intent_001",
    "intent_type": "analysis",
    "declared_goal": "Summarize community-authored knowledge responsibly.",
}

TEST_ACTOR = OtherPowers_ActorRef(
    actor_id="test_human_001",
    actor_type="human",
)

def main() -> None:
    print("\n[TEST] Running OtherPowers Intent Gate smoke test...\n")

    gate = OtherPowers_IntentGate(
        accountability_ledger_path=(
            "otherpowers_governance/accountability/data/ledgers/"
            "intent_decisions.jsonl"
        ),
        record_decisions=True,
    )

    decision = gate.evaluate_intent(
        intent=TEST_INTENT,
        actor=TEST_ACTOR,
        privacy_mode=OtherPowers_PrivacyMode.stealth,
    )

    print("[RESULT]")
    print(f"Decision: {decision.decision}")
    print(f"Rationale: {decision.rationale}")

    print("\n[OK] Intent gate smoke test completed successfully.\n")

if __name__ == "__main__":
    main()


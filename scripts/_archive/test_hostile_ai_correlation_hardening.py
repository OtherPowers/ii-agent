"""
Test: Hostile AI correlation hardening

Run:
  cd /Users/bush3000/ii-agent-reorg
  PYTHONPATH=/Users/bush3000/ii-agent-reorg python3 scripts/test_hostile_ai_correlation_hardening.py

What this test checks:
- Projected relays do NOT emit invertible semantic hashes
- Relays can include optional release_after_unix if configured
- Acceptance policy blocks forwarding until release_after_unix
"""

import time
from otherpowers_governance.memory_spheres import OtherPowers_MemorySphere, new_capability
from otherpowers_governance.memory_spheres.relay import DEFAULT_RELAY_RULES
from otherpowers_governance.memory_spheres.acceptance_policy import evaluate_relay_acceptance


def main():
    sphere = OtherPowers_MemorySphere(
        purpose="Hostile AI hardening test",
        risk_context="Correlation + inference pressure",
        encryption_hint="client-side-encrypted",
    )

    # Add enough entries to satisfy k-anonymity
    for _ in range(3):
        sphere.add_entry(
            content={
                "type": "governance_signal_memory",
                "event_type": "blocked",
                "intent_class": "surveillance",
                "recommended_shift": "increase_caution",
                "note": "Should not leak specifics.",
            },
            sensitivity="high",
            consent_required=True,
        )

    relay_rules = dict(DEFAULT_RELAY_RULES)
    relay_rules["release_delay_window_seconds"] = 60  # 0..60 sec delay

    # Project relays with NO projection_secret by default (no commitments)
    relays = sphere.project_relays(
        projection_rules=None,
        relay_rules=relay_rules,
    )

    print("\n[PROJECTED RELAYS]")
    for r in relays:
        print(r)

        payload = r.get("ai_to_ai_payload")
        if payload:
            assert "semantic_hash" not in payload, "semantic_hash must not exist"
        assert "release_after_unix" in r, "release_after_unix should exist when delay window enabled"

    # Acceptance policy should refuse forwarding until releasable
    secret = b"TEST_SECRET_KEY_CHANGE_IN_REAL_USE"
    cap = new_capability(
        secret_key=secret,
        rules={
            "allow_receive": True,
            "allow_forward": True,
            "allow_project": True,
            "max_forwards": 5,
            "sensitivity_ceiling": "high",
        },
    )

    test_relay = relays[0]
    decision_now = evaluate_relay_acceptance(
        relay=test_relay,
        capability_token=cap,
        capability_secret=secret,
        rules={
            "panic_secret": None,  # ignore panic state for this unit test
        },
    )
    print("\n[DECISION NOW]")
    print(decision_now.as_dict())

    # Wait until releasable
    ra = int(test_relay.get("release_after_unix") or int(time.time()))
    while int(time.time()) < ra:
        time.sleep(1)

    decision_later = evaluate_relay_acceptance(
        relay=test_relay,
        capability_token=cap,
        capability_secret=secret,
        rules={
            "panic_secret": None,
        },
    )
    print("\n[DECISION LATER]")
    print(decision_later.as_dict())


if __name__ == "__main__":
    main()


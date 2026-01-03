"""
Test: Poisoning + Flooding resistance

Run:
  cd /Users/bush3000/ii-agent-reorg
  PYTHONPATH=/Users/bush3000/ii-agent-reorg python3 scripts/test_poisoning_flooding_resistance.py

What this test simulates:
- A malicious actor spams relays of the same topic to drown warnings
- Our system should:
  - accept some (optional) but stop forwarding (quarantine)
  - rate-limit forwarding per capability
  - never crash
"""

import time

from otherpowers_governance.memory_spheres import OtherPowers_MemorySphere, new_capability
from otherpowers_governance.memory_spheres.relay import make_relay
from otherpowers_governance.memory_spheres.acceptance_policy import evaluate_relay_acceptance


def main():
    secret = b"TEST_SECRET_KEY_CHANGE_IN_REAL_USE"

    cap = new_capability(
        secret_key=secret,
        rules={
            "allow_receive": True,
            "allow_forward": True,
            "allow_project": True,
            "max_forwards": 999,
            "sensitivity_ceiling": "high",
        },
    )

    sphere = OtherPowers_MemorySphere(
        purpose="Poisoning/flooding test",
        risk_context="Relay spam pressure",
        encryption_hint="client-side-encrypted",
    )

    rules = {
        "panic_secret": None,  # do not couple this test to your local panic file
        "rate_limit_enabled": True,
        "accept_limit": 999,
        "accept_window_seconds": 60,
        "forward_limit": 999,
        "forward_window_seconds": 60,
        "topic_forward_limit": 5,           # SMALL on purpose for the test
        "topic_forward_window_seconds": 60, # 1 minute window
        "quarantine_accepts": True,
    }

    relays = []
    for i in range(12):
        relays.append(
            make_relay(
                topic_hint="censorship_pressure",
                signal_strength=0.6,
                recommended_posture="increase_caution",
                consent_required=True,
                sensitivity="high",
                rules={"release_delay_window_seconds": 0},
            )
        )

    print("\n[SPAM ATTEMPTS]")
    forwarded = 0
    quarantined = 0

    for idx, r in enumerate(relays):
        decision = evaluate_relay_acceptance(
            relay=r,
            capability_token=cap,
            capability_secret=secret,
            rules=rules,
        )

        if decision.forward:
            forwarded += 1
        if decision.reason in ("topic_quarantined_no_forward",):
            quarantined += 1

        print(f"[{idx}] {decision.as_dict()}")

    print("\n[SUMMARY]")
    print({"forwarded": forwarded, "quarantined": quarantined})

    assert forwarded <= 5, "Topic forward limiter failed (forwarded too many)"
    assert quarantined >= 1, "Expected quarantine to trigger at least once"

    print("\n[PASS] Flooding resistance works (topic quarantine + forward limiting).")


if __name__ == "__main__":
    main()


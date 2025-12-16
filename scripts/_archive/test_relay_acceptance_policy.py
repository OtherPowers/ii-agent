"""
Test: Relay Acceptance Policy

Run:
  cd /Users/bush3000/ii-agent-reorg
  PYTHONPATH=/Users/bush3000/ii-agent-reorg python3 scripts/test_relay_acceptance_policy.py
"""

from otherpowers_governance.memory_spheres import (
    OtherPowers_MemorySphere,
    new_capability,
)
from otherpowers_governance.memory_spheres.relay import make_relay


def main():
    secret = b"TEST_SECRET_KEY_CHANGE_IN_REAL_USE"

    cap = new_capability(
        secret_key=secret,
        rules={
            "allow_receive": True,
            "allow_forward": True,
            "allow_project": False,
            "max_forwards": 1,
            "sensitivity_ceiling": "medium",
        },
    )

    sphere = OtherPowers_MemorySphere(
        purpose="Acceptance policy test",
        risk_context="Simulated threat",
        encryption_hint="client-side-encrypted",
    )

    relay = make_relay(
        topic_hint="censorship_pressure",
        signal_strength=0.6,
        recommended_posture="increase_caution",
        consent_required=True,
        sensitivity="high",
    )

    print("\n[ATTEMPT RECEIVE — SHOULD FAIL (sensitivity ceiling)]")
    print(
        sphere.receive_relay_with_policy(
            relay=relay,
            capability_token=cap,
            capability_secret=secret,
        )
    )

    cap2 = new_capability(
        secret_key=secret,
        rules={
            "allow_receive": True,
            "allow_forward": True,
            "allow_project": True,
            "max_forwards": 1,
            "sensitivity_ceiling": "high",
        },
    )

    print("\n[ATTEMPT RECEIVE — SHOULD ACCEPT]")
    print(
        sphere.receive_relay_with_policy(
            relay=relay,
            capability_token=cap2,
            capability_secret=secret,
        )
    )

    print("\n[ATTEMPT FORWARD — SHOULD FORWARD ONCE]")
    forwarded = sphere.forward_relay_with_policy(
        relay=relay,
        capability_token=cap2,
        capability_secret=secret,
    )
    print(forwarded)

    print("\n[ATTEMPT FORWARD AGAIN — SHOULD FAIL]")
    forwarded2 = sphere.forward_relay_with_policy(
        relay=relay,
        capability_token=cap2,
        capability_secret=secret,
    )
    print(forwarded2)


if __name__ == "__main__":
    main()


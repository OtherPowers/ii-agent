"""
Test: Topic quarantine cool-down recovery (ISOLATED STATE)

Purpose:
- Ensure topic quarantine actually releases after cooldown
- Ensure forwarding resumes without manual reset
- Ensure no persistent soft-locks

Critical:
- Uses isolated disk paths
- Deletes state at start
"""

import os
import time

from otherpowers_governance.memory_spheres import new_capability
from otherpowers_governance.memory_spheres.relay import make_relay
from otherpowers_governance.memory_spheres.acceptance_policy import (
    evaluate_relay_acceptance,
)

TEST_RATE_LIMIT_PATH = "audit_logs/memory_spheres/_TEST_rate_limit_cooldown.json"
TEST_BUDGET_PATH = "audit_logs/memory_spheres/_TEST_capability_budget_cooldown.json"


def _rm(path: str) -> None:
    try:
        if os.path.isfile(path):
            os.remove(path)
    except Exception:
        pass


def main():
    # Ensure isolated, clean state
    _rm(TEST_RATE_LIMIT_PATH)
    _rm(TEST_BUDGET_PATH)

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

    rules = {
        # isolate disk state
        "rate_limit_path": TEST_RATE_LIMIT_PATH,
        "capability_budget_path": TEST_BUDGET_PATH,
        "panic_secret": None,

        "rate_limit_enabled": True,

        # Trigger quarantine quickly
        "topic_forward_limit": 2,
        "topic_forward_window_seconds": 10,

        # Small cooldown so test runs fast
        "quarantine_enabled": True,
        "quarantine_base_seconds": 5,
        "quarantine_max_seconds": 10,
        "quarantine_decay_after_seconds": 999999,

        # Avoid interference
        "accept_limit": 999,
        "accept_window_seconds": 60,
        "forward_limit": 999,
        "forward_window_seconds": 60,

        "quarantine_accepts": True,
    }

    def relay():
        return make_relay(
            topic_hint="censorship_pressure",
            signal_strength=0.6,
            recommended_posture="increase_caution",
            consent_required=True,
            sensitivity="high",
            rules={"release_delay_window_seconds": 0},
        )

    print("\n[FORWARD 1] should allow")
    d1 = evaluate_relay_acceptance(
        relay=relay(),
        capability_token=cap,
        capability_secret=secret,
        rules=rules,
    )
    print(d1.as_dict())
    assert d1.forward is True

    print("\n[FORWARD 2] should allow")
    d2 = evaluate_relay_acceptance(
        relay=relay(),
        capability_token=cap,
        capability_secret=secret,
        rules=rules,
    )
    print(d2.as_dict())
    assert d2.forward is True

    print("\n[FORWARD 3] should quarantine (no forward)")
    d3 = evaluate_relay_acceptance(
        relay=relay(),
        capability_token=cap,
        capability_secret=secret,
        rules=rules,
    )
    print(d3.as_dict())
    assert d3.forward is False

    print("\n[WAIT cooldown ~5s]")
    time.sleep(6)

    print("\n[FORWARD after cooldown] should allow again")
    d4 = evaluate_relay_acceptance(
        relay=relay(),
        capability_token=cap,
        capability_secret=secret,
        rules=rules,
    )
    print(d4.as_dict())
    assert d4.forward is True

    print("\n[PASS] Cool-down recovery works.")


if __name__ == "__main__":
    main()


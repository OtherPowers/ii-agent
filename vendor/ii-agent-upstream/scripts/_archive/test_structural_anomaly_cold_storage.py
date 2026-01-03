"""
Test: Structural anomaly -> cold storage (no forward)

Run:
  cd /Users/bush3000/ii-agent-reorg
  PYTHONPATH=/Users/bush3000/ii-agent-reorg python3 scripts/test_structural_anomaly_cold_storage.py
"""

import os

from otherpowers_governance.memory_spheres import new_capability
from otherpowers_governance.memory_spheres.acceptance_policy import evaluate_relay_acceptance
from otherpowers_governance.memory_spheres.relay import make_relay

TEST_RATE_LIMIT_PATH = "audit_logs/memory_spheres/_TEST_rate_limit_anomaly.json"
TEST_BUDGET_PATH = "audit_logs/memory_spheres/_TEST_capability_budget_anomaly.json"
TEST_COLD_STORAGE_PATH = "audit_logs/memory_spheres/_TEST_cold_storage.jsonl"


def _rm(path: str) -> None:
    try:
        if os.path.isfile(path):
            os.remove(path)
    except Exception:
        pass


def main():
    _rm(TEST_RATE_LIMIT_PATH)
    _rm(TEST_BUDGET_PATH)
    _rm(TEST_COLD_STORAGE_PATH)

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
        "panic_secret": None,
        "rate_limit_path": TEST_RATE_LIMIT_PATH,
        "capability_budget_path": TEST_BUDGET_PATH,

        "cold_storage_enabled": True,
        "cold_storage_path": TEST_COLD_STORAGE_PATH,
        "cold_storage_topic_hmac_secret": b"TEST_TOPIC_HMAC_SECRET",

        "anomaly_enabled": True,
        "anomaly_rules": {
            "cold_storage_threshold": 1,  # force routing for the test
            "expect_non_enumerable": True,
            "expect_non_coercive": True,
            "expect_bucketed_time_window": True,
            "expect_release_delay_present": True,
            "max_hops_reasonable_ceiling": 8,
            "signal_strength_high_threshold": 0.85,
        },

        # avoid interference
        "accept_limit": 999,
        "accept_window_seconds": 60,
        "forward_limit": 999,
        "forward_window_seconds": 60,
        "topic_forward_limit": 999,
        "topic_forward_window_seconds": 60,
        "quarantine_enabled": True,
        "quarantine_accepts": True,
    }

    # Construct a "structurally suspicious" relay:
    # - missing release delay expectation (we set release_delay_window_seconds=0)
    # - very high strength
    relay = make_relay(
        topic_hint="censorship_pressure",
        signal_strength=0.95,
        recommended_posture="increase_caution",
        consent_required=True,
        sensitivity="high",
        rules={"release_delay_window_seconds": 0},
    )

    decision = evaluate_relay_acceptance(
        relay=relay,
        capability_token=cap,
        capability_secret=secret,
        rules=rules,
    )

    print("\n[DECISION]")
    print(decision.as_dict())

    assert decision.accept is True
    assert decision.forward is False
    assert decision.reason == "routed_to_cold_storage"

    assert os.path.isfile(TEST_COLD_STORAGE_PATH), "cold storage file not written"
    with open(TEST_COLD_STORAGE_PATH, "r") as f:
        line = f.readline().strip()
    assert line, "cold storage record missing"

    print("\n[PASS] Anomaly routed to cold storage and blocked forwarding.")


if __name__ == "__main__":
    main()


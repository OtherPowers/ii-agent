"""
Test: Telemetry-free posture introspection does not leak internals.

Run:
  cd /Users/bush3000/ii-agent-reorg
  PYTHONPATH=/Users/bush3000/ii-agent-reorg python3 scripts/test_posture_introspection_safe.py
"""

from otherpowers_governance.signals import (
    OtherPowers_GovernanceSignal,
    OtherPowers_PostureAccumulator,
    build_posture_report,
    render_posture_text,
)

FORBIDDEN_SUBSTRINGS = [
    "signal_id",
    "source",
    "topic",
    "relay",
    "capability",
    "agent_id",
]

def main():
    acc = OtherPowers_PostureAccumulator(agent_salt="introspection_test")

    sig = OtherPowers_GovernanceSignal(
        posture="high_caution",
        source="unit_test_source_should_not_leak",
        recommended_actions={"slowdown": True},
        metadata={"topic_hint": "should_not_leak"},
    )
    acc.ingest(sig.as_dict())

    posture_state = acc.current_recommendation()
    report = build_posture_report(
        posture_state=posture_state,
        system_id="ii-agent",
        include_score_hint=True,
    )
    text = render_posture_text(report)

    print("\n[REPORT DICT]")
    print(report)
    print("\n[REPORT TEXT]")
    print(text)

    blob = (str(report) + "\n" + str(text)).lower()
    for bad in FORBIDDEN_SUBSTRINGS:
        assert bad not in blob

    assert report["posture"] == "high_caution"
    assert 0.0 <= float(report["confidence"]) <= 1.0

    print("\n[PASS] Introspection is safe and telemetry-free.")

if __name__ == "__main__":
    main()


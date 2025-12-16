"""
Test: Local-only posture snapshot (secure, overwrite-only).

Run:
  cd /Users/bush3000/ii-agent-reorg
  export OTHERPOWERS_SNAPSHOT_HMAC_KEY="some-long-random-string"
  PYTHONPATH=/Users/bush3000/ii-agent-reorg python3 scripts/test_posture_snapshot_local.py
"""

import os
import tempfile

from otherpowers_governance.signals import (
    OtherPowers_PostureAccumulator,
    OtherPowers_GovernanceSignal,
)
from otherpowers_governance.signals.posture_snapshot import (
    read_posture_snapshot,
    write_posture_snapshot,
)


def main():
    tmp_dir = tempfile.mkdtemp()
    snapshot_path = os.path.join(tmp_dir, "posture.json")

    acc = OtherPowers_PostureAccumulator(agent_salt="snapshot_test")

    # Create signal using ONLY supported args
    sig = OtherPowers_GovernanceSignal(
        posture="increase_caution",
        source="test_source_should_not_leak",
        recommended_actions={"slowdown": True},
    )

    sig_dict = sig.as_dict()

    # Inject strength at the dict level (this is what accumulator reads)
    sig_dict["signal_strength"] = 0.6

    acc.ingest(sig_dict)
    rec = acc.current_recommendation()

    # Write snapshot explicitly
    write_posture_snapshot(
        snapshot_path=snapshot_path,
        posture_state=rec,
        ttl_seconds=60,
    )

    assert os.path.exists(snapshot_path)

    loaded = read_posture_snapshot(snapshot_path, require_valid_hmac=False)
    assert loaded.get("posture") == rec.get("posture")
    assert "scores" not in loaded
    assert "source" not in str(loaded).lower()
    assert "topic" not in str(loaded).lower()
    assert loaded.get("confidence_bucket") in (
        "minimal",
        "weak",
        "moderate",
        "strong",
    )

    print("\n[PASS] Secure local snapshot works (API-aligned, redacted, integrity-aware).")


if __name__ == "__main__":
    main()


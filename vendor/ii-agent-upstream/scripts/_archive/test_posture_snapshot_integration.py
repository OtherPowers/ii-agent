"""
Test: accumulator writes secure snapshot automatically (overwrite-only).

Run:
  cd /Users/bush3000/ii-agent-reorg
  export OTHERPOWERS_SNAPSHOT_HMAC_KEY="$(python3 -c 'import secrets; print(secrets.token_urlsafe(48))')"
  PYTHONPATH=/Users/bush3000/ii-agent-reorg python3 scripts/test_posture_snapshot_integration.py
"""

import os
import tempfile

from otherpowers_governance.signals import (
    OtherPowers_PostureAccumulator,
    OtherPowers_GovernanceSignal,
)
from otherpowers_governance.signals.posture_snapshot import read_posture_snapshot


def main():
    tmp_dir = tempfile.mkdtemp()
    snapshot_path = os.path.join(tmp_dir, "posture.json")

    acc = OtherPowers_PostureAccumulator(
        agent_salt="snapshot_integration_test",
        snapshot_path=snapshot_path,
    )

    sig = OtherPowers_GovernanceSignal(
        posture="high_caution",
        source="integration_test_source_should_not_leak",
        recommended_actions={"local_only": True},
    )

    sig_dict = sig.as_dict()
    sig_dict["signal_strength"] = 0.8  # transport metadata, not constructor arg

    acc.ingest(sig_dict)

    rec = acc.current_recommendation()
    assert rec["posture"] in ("normal", "increase_caution", "high_caution", "freeze")

    assert os.path.exists(snapshot_path), "snapshot file was not created"

    loaded = read_posture_snapshot(snapshot_path, require_valid_hmac=False)
    assert loaded.get("posture") == rec.get("posture")
    assert loaded.get("confidence_bucket") in ("minimal", "weak", "moderate", "strong")
    assert "scores" not in loaded
    assert "source" not in str(loaded).lower()
    assert "topic" not in str(loaded).lower()

    if os.environ.get("OTHERPOWERS_SNAPSHOT_HMAC_KEY"):
        strict = read_posture_snapshot(snapshot_path, require_valid_hmac=True)
        assert strict.get("integrity_verified") is True

    print("\n[PASS] Accumulator snapshot integration works (secure + overwrite-only).")


if __name__ == "__main__":
    main()


import os

from otherpowers_governance.intelligence.influence_spine_adapter import (
    InfluenceSpineAdapter,
)

SNAPSHOT_PATH = "/Users/bush3000/ii-agent-reorg/tmp/volatility.snapshot"
SILENCE_FIELD_PATH = "/tmp/otherpowers_silence.field"

# clean start
if os.path.exists(SNAPSHOT_PATH):
    os.remove(SNAPSHOT_PATH)

if os.path.exists(SILENCE_FIELD_PATH):
    os.remove(SILENCE_FIELD_PATH)

adapter = InfluenceSpineAdapter()

result = adapter.process(
    {"pattern_families": ["volatility"]},
    snapshot_path=SNAPSHOT_PATH,
)

assert result is None, "Expected silence (None result)"
assert not os.path.exists(SNAPSHOT_PATH), "Snapshot should NOT be written"
assert os.path.exists(SILENCE_FIELD_PATH), "Silence field should be written"

print("OK: volatility → silence (tracked, no snapshot)")


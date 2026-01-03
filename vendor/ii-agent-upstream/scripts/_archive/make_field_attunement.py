import os

from otherpowers_governance.intelligence.influence_spine_adapter import InfluenceSpineAdapter

OUT = "/Users/bush3000/ii-agent-reorg/tmp/posture.field_state"

os.makedirs("/Users/bush3000/ii-agent-reorg/tmp", exist_ok=True)

adapter = InfluenceSpineAdapter()
adapter.process(
    {"pattern_families": ["care"]},
    field_state_path=OUT,
)

print(f"wrote field_state: {OUT}")


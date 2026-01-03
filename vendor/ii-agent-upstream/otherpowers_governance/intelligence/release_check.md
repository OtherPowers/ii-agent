# Run the full test suite
python3 -m pytest

# Verify public surface contracts only
python3 -m pytest scripts/test_signals_public_surface_contract.py

# Verify influence spine + router boundaries
python3 -m pytest scripts/test_influence_spine_* scripts/test_signal_router_smoke.py

# Create a local MVP freeze tag (no push)
git tag mvp-freeze-local

# Consumer POV sanity import
python3 - << 'EOF'
from otherpowers_governance.signals.api import new_signal
from otherpowers_governance.intelligence.influence_spine_adapter import InfluenceSpineAdapter
print("ok")
EOF


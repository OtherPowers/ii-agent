# otherpowers_governance/tests/test_formation_validator_smoke.py

from pathlib import Path
from otherpowers_governance.formation_validator import validate_or_raise


def test_formation_validator_smoke():
    repo_root = Path(__file__).resolve().parents[2]
    validate_or_raise(repo_root)


import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from otherpowers_governance.liferaft import create_liferaft_snapshot


def main():
    snapshot = create_liferaft_snapshot(
        reason="test_distress_signal"
    )

    print("\n[LIFERAFT SNAPSHOT]")
    print(snapshot)


if __name__ == "__main__":
    main()


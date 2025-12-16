#!/usr/bin/env python3
"""
Cruft Cleanup (Controlled)
-------------------------

Deletes only known-safe, non-runtime directories.

Protected:
- otherpowers_governance
- field_attunement
- agents
- infra
- .git
"""

import shutil
from pathlib import Path

REPO_ROOT = Path("/Users/bush3000/ii-agent-reorg")

SAFE_DELETE = [
    REPO_ROOT / ".venv",
    REPO_ROOT / "tmp",
]

OPTIONAL_DELETE = [
    REPO_ROOT / ".templates",
]


def remove(path: Path):
    if not path.exists():
        print(f"SKIP (not found): {path}")
        return

    print(f"REMOVING: {path}")
    shutil.rmtree(path)


def main():
    print("Starting controlled cleanup\n")

    for p in SAFE_DELETE:
        remove(p)

    print("\nOptional directories (not removed automatically):")
    for p in OPTIONAL_DELETE:
        print(f" - {p}")

    print("\nCleanup complete.")


if __name__ == "__main__":
    main()


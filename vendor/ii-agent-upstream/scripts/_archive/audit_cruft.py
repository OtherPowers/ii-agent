#!/usr/bin/env python3
"""
Cruft Audit (Dry Run)
--------------------

Identifies large experimental directories that are safe candidates
for removal WITHOUT deleting anything.

Nothing destructive happens here.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

KEEP_DIRS = {
    "otherpowers_governance",
    "field_attunement",
    "agents",
    "infra",
    "docs",
    "scripts",
}

CRUFT_HINTS = (
    "perception",
    "dispatch",
    "experiment",
    "experiments",
    "scratch",
    "tmp",
    "test",
    "tests",
    "sandbox",
    "archive",
)

def main():
    print("Cruft audit (dry run)")
    print("=====================\n")

    candidates = []

    for p in REPO_ROOT.iterdir():
        if not p.is_dir():
            continue

        if p.name in KEEP_DIRS:
            continue

        lowered = p.name.lower()
        if any(hint in lowered for hint in CRUFT_HINTS):
            candidates.append(p)

    if not candidates:
        print("No obvious cruft directories found.")
        return

    for c in sorted(candidates):
        try:
            count = sum(1 for _ in c.rglob("*"))
        except Exception:
            count = "unknown"

        print(f"- {c.name}/  ({count} files)")

    print("\nNothing deleted.")
    print("If this list looks right, we can remove them in one controlled pass.")


if __name__ == "__main__":
    main()


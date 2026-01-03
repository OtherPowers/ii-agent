#!/usr/bin/env python3
"""
OtherPowers governance sanity runner.

Goal:
- Confirm the governance tree is sane (no nested otherpowers_governance/otherpowers_governance).
- Confirm required spec/docs exist (ai-to-ai).
- Import every Python module under otherpowers_governance/{filters,evaluations,intelligence,liferaft,accountability}.
- Optionally emit one accountability event into the ledger (if module exists).

Run from repo root:
  python3 scripts/run_otherpowers_governance_check.py

Or from anywhere:
  python3 /path/to/ii-agent-reorg/scripts/run_otherpowers_governance_check.py
"""

from __future__ import annotations

import importlib
import json
import os
import sys
from pathlib import Path
from typing import List, Tuple


REQUIRED_PATHS = [
    "otherpowers_governance/__init__.py",
    "otherpowers_governance/ai-to-ai/multi-agent-negotiation-rules.md",
    "otherpowers_governance/ai-to-ai/structured-message-format.yaml",
    "otherpowers_governance/ai-to-ai/intent_embedding_schema.json",
]

OPTIONAL_IMPORT_ROOTS = [
    "otherpowers_governance.filters",
    "otherpowers_governance.evaluations",
    "otherpowers_governance.intelligence",
    "otherpowers_governance.liferaft",
    "otherpowers_governance.accountability",
]


def _find_repo_root(start: Path) -> Path:
    """
    Find repo root by searching upward for 'otherpowers_governance' folder.
    """
    cur = start.resolve()
    for _ in range(20):
        if (cur / "otherpowers_governance").exists():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    raise RuntimeError("Could not locate repo root containing 'otherpowers_governance/'.")


def _fail(msg: str) -> None:
    print(f"[FAIL] {msg}")
    raise SystemExit(1)


def _warn(msg: str) -> None:
    print(f"[WARN] {msg}")


def _ok(msg: str) -> None:
    print(f"[OK]   {msg}")


def _check_tree_sanity(repo_root: Path) -> None:
    gov_root = repo_root / "otherpowers_governance"
    nested = gov_root / "otherpowers_governance"
    if nested.exists():
        _fail(
            "Nested folder detected: otherpowers_governance/otherpowers_governance/. "
            "Move its contents up one level and delete the nested folder."
        )
    _ok("No nested governance root detected.")


def _check_required_paths(repo_root: Path) -> None:
    missing = []
    for rel in REQUIRED_PATHS:
        p = repo_root / rel
        if not p.exists():
            missing.append(rel)
    if missing:
        _fail("Missing required governance files:\n  - " + "\n  - ".join(missing))
    _ok("Required governance files present.")

    # Validate JSON files are parseable (no external deps)
    intent_schema = repo_root / "otherpowers_governance/ai-to-ai/intent_embedding_schema.json"
    try:
        json.loads(intent_schema.read_text(encoding="utf-8"))
        _ok("intent_embedding_schema.json parses cleanly.")
    except Exception as e:
        _fail(f"intent_embedding_schema.json is not valid JSON: {e}")


def _iter_py_modules(repo_root: Path, pkg_root: str) -> List[str]:
    """
    Discover importable modules under a package by walking the filesystem.
    """
    parts = pkg_root.split(".")
    pkg_dir = repo_root.joinpath(*parts)
    if not pkg_dir.exists():
        _warn(f"Package folder not found on disk: {pkg_dir}")
        return []

    modules: List[str] = []
    for path in pkg_dir.rglob("*.py"):
        if path.name == "__pycache__":
            continue
        if "__pycache__" in path.parts:
            continue
        rel = path.relative_to(repo_root)
        mod = ".".join(rel.with_suffix("").parts)
        modules.append(mod)
    # Prefer deterministic order
    modules = sorted(set(modules))
    return modules


def _import_modules(modules: List[str]) -> Tuple[List[str], List[Tuple[str, str]]]:
    ok: List[str] = []
    bad: List[Tuple[str, str]] = []
    for m in modules:
        try:
            importlib.import_module(m)
            ok.append(m)
        except Exception as e:
            bad.append((m, repr(e)))
    return ok, bad


def _maybe_emit_accountability_event(repo_root: Path) -> None:
    """
    If the accountability module exists, write one small event to the ledger.
    This is a smoke test, not production behavior.
    """
    try:
        from otherpowers_governance.accountability.models import (
            OtherPowers_ActorRef,
            OtherPowers_PrivacyMode,
            OtherPowers_AccountabilityEvent,
            OtherPowers_now_iso,
        )
        from otherpowers_governance.accountability.ledger import OtherPowers_AppendOnlyLedger
    except Exception as e:
        _warn(f"Skipping accountability emission (module not importable yet): {e}")
        return

    ledger_path = repo_root / "otherpowers_governance/accountability/data/ledgers/accountability_ledger.jsonl"
    ledger = OtherPowers_AppendOnlyLedger(str(ledger_path))

    actor = OtherPowers_ActorRef(
        actor_id="individual_smoke_001",
        actor_type="individual",
        display_name=None,
        privacy_mode=OtherPowers_PrivacyMode.stealth,
    )

    evt = OtherPowers_AccountabilityEvent(
        event_id="acct_evt_smoke_001",
        created_at=OtherPowers_now_iso(),
        actor=actor,
        privacy_mode=OtherPowers_PrivacyMode.stealth,
        sphere_id=None,
        title="Governance smoke test event",
        statement="A minimal append-only event written by the governance sanity runner.",
        tags=["smoke_test", "anti_erasure", "care"],
        receipts=[],
        affected_groups_self_defined=[],
        context={"tool": "run_otherpowers_governance_check.py"},
        harm_prevention_flags={"visibility": "community"},
    ).finalize()

    ledger.append(evt.to_record())
    _ok(f"Wrote accountability smoke event to: {ledger_path}")


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    repo_root = _find_repo_root(script_dir)

    # Ensure repo root on sys.path for imports
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    print(f"Repo root: {repo_root}")
    _check_tree_sanity(repo_root)
    _check_required_paths(repo_root)

    # Discover + import all python modules in governance packages
    all_modules: List[str] = []
    for pkg in OPTIONAL_IMPORT_ROOTS:
        discovered = _iter_py_modules(repo_root, pkg)
        if discovered:
            _ok(f"Discovered {len(discovered)} modules under {pkg}")
        else:
            _warn(f"No modules discovered under {pkg} (folder missing or empty).")
        all_modules.extend(discovered)

    ok_mods, bad_mods = _import_modules(sorted(set(all_modules)))
    _ok(f"Imported {len(ok_mods)} governance modules.")

    if bad_mods:
        print("\n[FAIL] Import errors:")
        for m, err in bad_mods:
            print(f"  - {m}: {err}")
        raise SystemExit(1)

    _maybe_emit_accountability_event(repo_root)
    print("\n[OK] Governance sanity runner completed successfully.")


if __name__ == "__main__":
    main()


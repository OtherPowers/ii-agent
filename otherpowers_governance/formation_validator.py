from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List
import re


GOVERNANCE_ROOT = "otherpowers_governance"
ALLOWED_SUFFIX = ".py"

# Files that are exempt from scanning (self + registries)
SELF_EXEMPT_FILES = {
    "formation_validator.py",
    "registry.py",
}

# Tokens that represent *actual* control surfaces when used in executable logic
CONTROL_TOKENS = (
    "enforce",
    "authorize",
    "deny",
    "permission",
    "access_control",
    "telemetry",
    "monitor",
    "profile",
    "identify",
    "track_user",
)

# Conceptual / descriptive vocabulary that must never trigger
ALLOWLIST_TOKENS = (
    "utility",
    "horizon",
    "legibility",
    "inspiration",
    "exposure",
    "lineage",
    "care",
    "non_extractive",
)

NEGATION_MARKERS = (
    "no ",
    "not ",
    "never ",
    "non-",
    "without ",
)


@dataclass(frozen=True)
class FormationFinding:
    path: str
    line: int
    kind: str
    snippet: str


class FormationValidator:
    def scan_repo(self, repo_root: str | Path) -> List[FormationFinding]:
        root = Path(repo_root)
        findings: List[FormationFinding] = []

        gov_root = root / GOVERNANCE_ROOT
        if not gov_root.exists():
            return []

        for path in gov_root.rglob(f"*{ALLOWED_SUFFIX}"):
            if path.name in SELF_EXEMPT_FILES:
                continue
            findings.extend(self._scan_file(path))

        return findings

    def _scan_file(self, path: Path) -> Iterable[FormationFinding]:
        results: List[FormationFinding] = []

        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except Exception:
            return results

        in_docstring = False

        for lineno, raw in enumerate(lines, start=1):
            line = raw.strip()
            lower = line.lower()

            # Skip comments
            if line.startswith("#"):
                continue

            # Handle docstrings
            if line.startswith(('"""', "'''")):
                in_docstring = not in_docstring
                continue
            if in_docstring:
                continue

            # Skip empty lines
            if not line:
                continue

            # Skip constant lists / registries
            if "=" in line and "(" in line and ")" in line:
                continue

            # Ignore allow-listed conceptual language
            if any(tok in lower for tok in ALLOWLIST_TOKENS):
                continue

            # Ignore negated language
            if any(marker in lower for marker in NEGATION_MARKERS):
                continue

            # Flag only executable control usage
            for token in CONTROL_TOKENS:
                if re.search(rf"\b{token}\b", lower):
                    results.append(
                        FormationFinding(
                            path=str(path),
                            line=lineno,
                            kind="control_surface",
                            snippet=raw.strip(),
                        )
                    )

        return results


def validate_or_raise(repo_root: str | Path) -> None:
    validator = FormationValidator()
    findings = validator.scan_repo(repo_root)

    if not findings:
        return

    rendered = "\n".join(
        f"{f.path}:{f.line} [{f.kind}] {f.snippet}"
        for f in findings[:80]
    )

    raise AssertionError(
        "FormationValidator detected active governance control surfaces:\n"
        + rendered
        + ("\n…(truncated)" if len(findings) > 80 else "")
    )


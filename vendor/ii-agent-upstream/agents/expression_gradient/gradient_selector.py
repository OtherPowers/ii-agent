"""
Expression gradient selector.

Determines the appropriate expression depth
for a governance response based on context
and relational signals.
"""

from typing import Dict


def select_expression_layer(
    *,
    governance_result: Dict,
    agent_context: Dict | None = None,
) -> int:
    """
    Returns an integer representing expression depth.

    Lower = more minimal / legacy-compatible
    Higher = more relational / ethical / expansive

    This function must be fast, deterministic,
    and safe to downshift at any time.
    """

    agent_context = agent_context or {}

    status = governance_result.get("overall_status")
    historical_alignment = agent_context.get("alignment_history", 0)
    extraction_pressure = agent_context.get("extraction_pressure", "unknown")
    care_signals = agent_context.get("care_signals", False)

    # Hard safety first: FAIL collapses expression depth
    if status == "fail":
        return 1

    # REVIEW keeps things grounded but contextual
    if status == "review":
        return 2

    # PASS can expand based on relational signals
    if status == "pass":
        if care_signals and historical_alignment >= 3:
            return 4
        if care_signals:
            return 3
        return 2

    # Defensive fallback
    return 1

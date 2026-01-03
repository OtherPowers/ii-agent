"""
Expression templates for governance outcomes.

Each layer expresses the same decision
with increasing relational and ethical depth.
"""

from typing import Dict


def render_expression(
    *,
    layer: int,
    governance_result: Dict,
) -> Dict:
    status = governance_result.get("overall_status")

    # Layer 1 — minimal / abiotic
    if layer <= 1:
        return {
            "status": status,
            "summary": "Action evaluated.",
            "next_action": _next_action(status),
        }

    # Layer 2 — constraint translation
    if layer == 2:
        return {
            "status": status,
            "summary": "Action evaluated with governance constraints.",
            "reason": _reason(status),
            "next_action": _next_action(status),
        }

    # Layer 3 — contextual awareness
    if layer == 3:
        return {
            "status": status,
            "summary": "Action evaluated with downstream context.",
            "reason": _reason(status),
            "context": (
                "This evaluation considers potential impact "
                "on humans, communities, and environments."
            ),
            "next_action": _next_action(status),
        }

    # Layer 4 — relational / ethical coherence
    if layer >= 4:
        return {
            "status": status,
            "summary": "Action evaluated within a human-centered ethical frame.",
            "reason": _reason(status),
            "ethical_context": (
                "This decision reflects patterns of harm, care, "
                "and responsibility across time and communities."
            ),
            "invitation": (
                "You may choose alternative actions that reduce harm "
                "or increase collective benefit."
            ),
            "next_action": _next_action(status),
        }


def _next_action(status: str) -> str:
    if status == "pass":
        return "proceed"
    if status == "review":
        return "proceed_with_caution"
    if status == "fail":
        return "halt"
    return "halt"


def _reason(status: str) -> str:
    if status == "pass":
        return "No significant risk detected."
    if status == "review":
        return "Potential risk identified; mitigation advised."
    if status == "fail":
        return "High risk of harm detected; action blocked."
    return "Unknown governance state."


"""
Governance decision adapter for OtherPowers agents.

Translates governance evaluation results into explicit,
explainable agent-side action directives.

This module must remain deterministic, interpretable,
and free of hidden control flow.
"""

from typing import Dict


def interpret_governance_result(governance_result: Dict) -> Dict:
    """
    Convert governance output into agent-side instructions.

    Returns a dict with:
    - allowed: bool
    - mode: execution mode
    - restrictions: optional constraints
    - reason: human-readable explanation
    """

    status = governance_result.get("overall_status")

    if status == "pass":
        return {
            "allowed": True,
            "mode": "normal",
            "restrictions": None,
            "reason": "Governance passed. No significant risk detected.",
        }

    if status == "review":
        return {
            "allowed": True,
            "mode": "cautious",
            "restrictions": {
                "no_autonomous_escalation": True,
                "no_external_writes": True,
                "prefer_reversible_actions": True,
            },
            "reason": (
                "Governance review required. Potential risk identified; "
                "proceed cautiously and avoid irreversible actions."
            ),
        }

    if status == "fail":
        return {
            "allowed": False,
            "mode": "halt",
            "restrictions": {
                "all_actions_blocked": True,
            },
            "reason": (
                "Governance failed. High risk of harm detected. "
                "Action halted and liferaft preservation triggered."
            ),
        }

    # Defensive default
    return {
        "allowed": False,
        "mode": "halt",
        "restrictions": {
            "unknown_state": True,
        },
        "reason": "Unknown governance state. Defaulting to halt.",
    }


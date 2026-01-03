"""
Example agent implementation for demonstrating
OtherPowers governance enforcement and expression gradients.
"""

from typing import Dict, Any


class ExampleAgent:
    def act(
        self,
        payload: Dict[str, Any],
        governance: Dict,
        expression: Dict,
    ) -> Dict[str, Any]:
        return {
            "status": "executed",
            "mode": "normal",
            "message": "Action executed normally.",
            "expression": expression,
            "governance_status": governance.get("overall_status"),
        }

    def act_cautiously(
        self,
        payload: Dict[str, Any],
        restrictions: Dict[str, Any],
        governance: Dict,
        expression: Dict,
    ) -> Dict[str, Any]:
        return {
            "status": "executed_with_caution",
            "mode": "cautious",
            "restrictions": restrictions,
            "message": "Action executed with safeguards.",
            "expression": expression,
            "governance_status": governance.get("overall_status"),
        }


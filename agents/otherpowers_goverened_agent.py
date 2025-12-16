"""
OtherPowers Governed Agent Wrapper.

Ensures all agent actions are evaluated through governance,
interpreted via decision adapters, and expressed through
the expression gradient before execution.
"""

from typing import Any, Dict

from otherpowers_governance.evaluations.eval_harness import run_full_evaluation
from backend.agents.governance_decision_adapter import (
    interpret_governance_result,
)
from backend.agents.expression_gradient.gradient_selector import (
    select_expression_layer,
)
from backend.agents.expression_gradient.gradient_templates import (
    render_expression,
)


class OtherPowersGovernedAgent:
    """
    Wraps an underlying agent and enforces governance
    before any action is taken.
    """

    def __init__(self, agent):
        self.agent = agent

    def act(
        self,
        payload: Dict[str, Any],
        agent_context: Dict | None = None,
    ) -> Dict[str, Any]:
        """
        Evaluate governance, interpret decision,
        select expression depth, and conditionally
        execute agent action.
        """

        governance_result = run_full_evaluation(payload)
        decision = interpret_governance_result(governance_result)

        layer = select_expression_layer(
            governance_result=governance_result,
            agent_context=agent_context,
        )

        expression = render_expression(
            layer=layer,
            governance_result=governance_result,
        )

        if not decision["allowed"]:
            return {
                "status": "halted",
                "expression": expression,
                "governance": governance_result,
            }

        if decision["mode"] == "cautious":
            return self.agent.act_cautiously(
                payload=payload,
                restrictions=decision["restrictions"],
                governance=governance_result,
                expression=expression,
            )

        return self.agent.act(
            payload=payload,
            governance=governance_result,
            expression=expression,
        )


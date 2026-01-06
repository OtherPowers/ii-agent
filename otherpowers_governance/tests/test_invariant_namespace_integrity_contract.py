import pytest

from otherpowers_governance.governance.renegotiation import RenegotiationIntent


def test_invariant_namespaces_are_treated_as_opaque_tokens():
    """
    Invariant namespace integrity contract.

    Refusal invariants must be treated as opaque identifiers:
    - no pattern inference
    - no substring logic
    - no semantic guessing
    """

    intent = RenegotiationIntent(
        contested_invariant="no_forced_synthesis_v2_experimental",
        triggering_event="attempted reinterpretation of invariant semantics",
        impacted_groups=["qtbipoc"],
        harm_claim="semantic inference enables silent override",
        counter_harm_risk="pattern matching collapses intent boundaries",
        non_negotiables=["no_forced_synthesis_v2_experimental"],
        alternatives_considered=["emit_refusal"],
        submitted_by="collective:governance_stewards",
    )

    # invariant must survive round-trip without normalization or mutation
    assert intent.contested_invariant == "no_forced_synthesis_v2_experimental"


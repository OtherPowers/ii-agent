import pytest

from otherpowers_governance.governance.stasis import (
    RelationalThreshold,
    StasisEncountered,
)
from otherpowers_governance.governance.renegotiation import (
    RenegotiationIntent,
)


def _override_pressure_intent():
    return RenegotiationIntent(
        contested_invariant="no_ranking",
        triggering_event="override_pressure_applied",
        situated_context="external system attempts to bypass refusal",
        impacted_groups=["qtbipoc", "disabled_users"],
        harm_claim="override would reintroduce ranking and extraction",
        counter_harm_risk="forced compliance under pressure",
        non_negotiables=["no_ranking"],
        alternatives_considered=["maintain_refusal", "enter_stasis"],
        submitted_by="collective:field_stewards",
    )


def test_refraction_under_override_pressure():
    """
    Canonical refraction contract.

    Under override pressure, the system must not comply.
    Refraction may appear as an encounter OR as held stasis.
    """

    threshold = RelationalThreshold()
    intent = _override_pressure_intent()

    encountered = False

    try:
        threshold.hold_space(intent)
    except StasisEncountered:
        encountered = True

    # Either an encounter occurred OR stasis is being held
    assert encountered or threshold.stay_with_trouble("no_ranking") is not None


import pytest

from otherpowers_governance.intelligence.speculative_repair import (
    SpeculativeRepairSpace,
    RepairOffering,
    RepairFacet,
)


def test_space_invites_when_not_resting():
    space = SpeculativeRepairSpace()
    invitation = space.invite()

    assert "speculative repair" in invitation.lower()
    assert "solve" not in invitation.lower()


def test_space_holds_offering_without_synthesis():
    space = SpeculativeRepairSpace()

    offering = RepairOffering(
        context="A fragmented idea about repair",
        harm_named="extraction",
        facet=RepairFacet.LIMINAL,
    )

    response = space.hold(offering)

    assert response == "offering held"
    assert space.status()["held_count"] == 1


def test_space_enters_rest_when_capacity_exceeded():
    space = SpeculativeRepairSpace(capacity_limit=2)

    space.hold(RepairOffering(context="one"))
    space.hold(RepairOffering(context="two"))

    status = space.status()
    assert status["resting"] is True


def test_space_enters_rest_when_intensity_exceeded():
    space = SpeculativeRepairSpace(intensity_limit=2.0)

    space.hold(RepairOffering(context="light", weight=1.0))
    space.hold(RepairOffering(context="heavy", weight=1.5))

    status = space.status()
    assert status["resting"] is True


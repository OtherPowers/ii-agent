from otherpowers_governance.intelligence.speculative_repair import (
    SpeculativeRepairSpace,
    RepairOffering,
)


def test_compost_clears_literal_content_but_preserves_availability():
    space = SpeculativeRepairSpace()

    space.hold(RepairOffering(context="Something unresolved"))
    assert space.status()["held_count"] == 1

    space.compost()

    status = space.status()
    assert status["held_count"] == 0
    assert status["current_intensity"] == 0.0


def test_rest_prevents_further_holding():
    space = SpeculativeRepairSpace(capacity_limit=1)

    space.hold(RepairOffering(context="first"))
    assert space.status()["resting"] is True

    response = space.hold(RepairOffering(context="second"))
    assert response == "space resting"


def test_resume_allows_activity_after_rest_and_compost():
    space = SpeculativeRepairSpace(capacity_limit=1)

    space.hold(RepairOffering(context="first"))
    assert space.status()["resting"] is True

    space.compost()
    space.resume()

    response = space.hold(RepairOffering(context="second"))
    assert response == "offering held"


from otherpowers_governance.intelligence.speculative_repair import (
    SpeculativeRepairSpace,
    RepairOffering,
)


def test_opaque_offerings_are_held_without_exposure():
    space = SpeculativeRepairSpace()

    opaque = RepairOffering(
        context="Sensitive lineage-bound thought",
        is_opaque=True,
    )

    response = space.hold(opaque)

    assert response == "offering held"

    status = space.status()

    # Opacity means: count may increase,
    # but no differentiation or exposure is implied
    assert status["held_count"] == 1
    assert "Sensitive lineage" not in str(status)


def test_opaque_and_non_opaque_are_not_distinguished_in_status():
    space = SpeculativeRepairSpace()

    space.hold(
        RepairOffering(
            context="Opaque thought",
            is_opaque=True,
        )
    )

    space.hold(
        RepairOffering(
            context="Non-opaque thought",
            is_opaque=False,
        )
    )

    status = space.status()

    # Status reports structure only, not content classes
    assert status["held_count"] == 2
    assert "opaque" not in str(status).lower()


def test_compost_removes_opaque_and_non_opaque_equally():
    space = SpeculativeRepairSpace()

    space.hold(RepairOffering(context="one", is_opaque=True))
    space.hold(RepairOffering(context="two", is_opaque=False))

    assert space.status()["held_count"] == 2

    space.compost()

    status = space.status()

    assert status["held_count"] == 0
    assert status["current_intensity"] == 0.0


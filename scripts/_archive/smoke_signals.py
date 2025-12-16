from otherpowers_governance.signals import (
    OtherPowers_GovernanceSignal,
    SignalKind,
    Posture,
)

sig = OtherPowers_GovernanceSignal(
    kind=SignalKind.GOVERNANCE,
    posture=Posture.NEUTRAL,
    signal_strength=0.5,
)

print("Smoke test OK:", sig.to_dict())


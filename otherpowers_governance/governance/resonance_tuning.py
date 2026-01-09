"""
Resonance Tuning

Resonance Tuning names how a field listens.
It describes when conditions are in harmony,
when they are still,
and when they are ready to unfold.

Nothing is forced.
Nothing is extracted.
The field responds only to what coheres.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ResonanceTuning:
    """
    Resonance Tuning describes the state of attunement
    between a field and what approaches it.

    It does not decide.
    It does not optimize.
    It simply reflects whether conditions align.
    """

    resonance: float
    override_pressure: bool = False

    def settles_into_silence(self) -> bool:
        """
        Silence occurs when alignment is absent
        or when pressure disrupts coherence.
        """
        return self.override_pressure or self.resonance <= 0.0

    def affirms_presence(self) -> bool:
        """
        Presence may be acknowledged
        when resonance is felt and unforced.
        """
        return not self.override_pressure and self.resonance > 0.0

    def invites_bloom(self) -> bool:
        """
        Bloom becomes possible only when resonance
        is dense, mutual, and unpressured.
        """
        return not self.override_pressure and self.resonance >= 1.0

    def carries_context(self) -> bool:
        """
        Context travels only when bloom is invited.
        """
        return self.invites_bloom()


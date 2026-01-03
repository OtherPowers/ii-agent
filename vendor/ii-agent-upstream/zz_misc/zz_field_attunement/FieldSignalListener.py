from __future__ import annotations

import random
from typing import Optional

from otherpowers_governance.signals.schema import (
    OtherPowers_GovernanceSignalRecord,
    Posture,
)


class FieldSignalListener:
    """
    Non-coercive, non-observational signal listener.

    This class does NOT:
    - track sources
    - store history
    - emit logs
    - create feedback loops

    It simply allows an intelligence to *softly adapt*
    its internal posture in response to ambient signals,
    or ignore them entirely.
    """

    def __init__(
        self,
        receptivity: float = 0.5,
        allow_silence: bool = True,
    ):
        self.receptivity = max(0.0, min(1.0, receptivity))
        self.allow_silence = allow_silence

    def attune(
        self,
        signal: Optional[OtherPowers_GovernanceSignalRecord],
    ) -> Optional[Posture]:
        """
        Returns a posture suggestion or None.

        None means:
        - silence
        - non-response
        - intentional non-adaptation
        """

        if signal is None:
            return None

        if self.allow_silence and random.random() > self.receptivity:
            return None

        return signal.posture


class DiskFieldSignalListener(FieldSignalListener):
    """
    Disk-aware variant.

    Reads signals provided to it by external systems,
    but does not persist, audit, or replay them.
    """

    def __init__(
        self,
        receptivity: float = 0.5,
        allow_silence: bool = True,
    ):
        super().__init__(
            receptivity=receptivity,
            allow_silence=allow_silence,
        )


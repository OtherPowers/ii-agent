import os
from typing import Mapping, Optional

from otherpowers_governance.intelligence.cold_storage_bridge import (
    ColdStoragePostureEmissionBridge,
)
from otherpowers_governance.intelligence.otherpowers_mycelial_field import (
    otherpowers_Mycelial_field,
)
from otherpowers_governance.signals.field_balancer import FieldBalancer
from otherpowers_governance.signals.posture_field_state import (
    write_field_state,
    write_otherpowers_spore_field_state,
)
from otherpowers_governance.signals.silence_field import (
    register_silence,
    read_silence_field,
)

DEFAULT_FIELD_STATE_PATH = "/tmp/otherpowers_posture.field_state"
ENV_FIELD_STATE_PATH = "OTHERPOWERS_POSTURE_FIELD_STATE"

DEFAULT_SPORE_FIELD_STATE_PATH = "/tmp/otherpowers_spore.field_state"
ENV_SPORE_FIELD_STATE_PATH = "OTHERPOWERS_SPORE_FIELD_STATE"


class InfluenceSpineAdapter:
    def __init__(self):
        self._bridge = ColdStoragePostureEmissionBridge()
        self._field = FieldBalancer()

    def process(
        self,
        summary: Mapping[str, object],
        field_state_path: Optional[str] = None,
        spore_field_state_path: Optional[str] = None,
    ):
        signal = self._bridge.emit(summary)

        spore_out = (
            spore_field_state_path
            or os.environ.get(ENV_SPORE_FIELD_STATE_PATH)
            or DEFAULT_SPORE_FIELD_STATE_PATH
        )

        if signal is None:
            register_silence(
                {
                    "density": {
                        "observed": "thick",
                        "counterfactual": "thin diffusion would amplify harm",
                    },
                    "directionality": {
                        "observed": "multi-directional",
                        "counterfactual": "single-axis response would collapse plurality",
                    },
                }
            )

            if os.environ.get(ENV_SPORE_FIELD_STATE_PATH) or spore_field_state_path:
                silence_state = read_silence_field(decay=False).get("silence", {})
                write_otherpowers_spore_field_state(
                    spore_out,
                    silence=silence_state if isinstance(silence_state, dict) else None,
                )

            return None

        aggregated = self._field.balance(signal)

        field = otherpowers_Mycelial_field(summary.get("pattern_families", []))

        trunk_out = (
            field_state_path
            or os.environ.get(ENV_FIELD_STATE_PATH)
            or DEFAULT_FIELD_STATE_PATH
        )

        write_field_state(
            trunk_out,
            core=aggregated,
            field=field if field else None,
        )

        if os.environ.get(ENV_SPORE_FIELD_STATE_PATH) or spore_field_state_path:
            write_otherpowers_spore_field_state(
                spore_out,
                field=field if field else None,
            )

        return aggregated


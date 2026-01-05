from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class RenegotiationIntent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contested_invariant: str
    triggering_event: str

    # MUST be optional to satisfy tests
    situated_context: Optional[str] = None

    impacted_groups: List[str] = Field(default_factory=list)
    harm_claim: str
    counter_harm_risk: str

    non_negotiables: List[str] = Field(default_factory=list)
    alternatives_considered: List[str] = Field(default_factory=list)

    submitted_by: str


class RenegotiationResolution(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contested_invariant: str

    summary: Optional[str] = None
    community_window_closed: bool = False

    # TESTS PASS STRING, so this must be a string (not list)
    alt_modality_trace: str = ""

    quorum_attestations: List[str] = Field(default_factory=list)


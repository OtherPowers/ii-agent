from __future__ import annotations

from dataclasses import dataclass
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class RenegotiationIntent(BaseModel):
    """
    Canonical intent object. This must exist before renegotiation proceeds.
    Designed to be hard to complete without real accountability.
    """
    model_config = ConfigDict(extra="forbid")

    contested_invariant: str = Field(..., min_length=1)
    triggering_event: str = Field(..., min_length=1)

    impacted_groups: List[str] = Field(..., min_length=1)

    harm_claim: str = Field(..., min_length=12)
    counter_harm_risk: str = Field(..., min_length=12)

    non_negotiables: List[str] = Field(..., min_length=1)
    alternatives_considered: List[str] = Field(..., min_length=1)

    # Must be an org/role/collective label, not an individual.
    submitted_by: str = Field(..., min_length=3)

    @field_validator("impacted_groups", "non_negotiables", "alternatives_considered")
    @classmethod
    def _no_blank_items(cls, v: List[str]) -> List[str]:
        if any((item or "").strip() == "" for item in v):
            raise ValueError("List fields cannot contain blank items.")
        return v

    @model_validator(mode="after")
    def _submitter_must_be_collective(self) -> "RenegotiationIntent":
        s = (self.submitted_by or "").strip()
        # Allow patterns like "collective:...", "role:...", "org:..."
        allowed_prefixes = ("collective:", "role:", "org:", "council:", "guild:")
        if not s.startswith(allowed_prefixes):
            raise ValueError(
                "submitted_by must be a collective/role/org label (e.g., 'collective:...'), not an individual."
            )
        return self


class RenegotiationResolution(BaseModel):
    """
    Resolution object required to exit stasis.
    Keeps this process forkable + contestable without admin overrides.
    """
    model_config = ConfigDict(extra="forbid")

    contested_invariant: str = Field(..., min_length=1)
    outcome: Literal["upheld", "amended", "forked", "dissolved"] = "upheld"
    summary: str = Field(..., min_length=12)

    community_window_closed: bool = False
    quorum_attestations: List[str] = Field(default_factory=list)

    # Only meaningful when outcome == "amended"
    new_invariant_version: Optional[str] = None

    @model_validator(mode="after")
    def _enforce_quorum_and_window(self) -> "RenegotiationResolution":
        if not self.community_window_closed:
            raise ValueError("community_window_closed must be True to finalize a resolution.")
        if len(self.quorum_attestations) < 2:
            raise ValueError("At least 2 quorum_attestations are required to prevent single-group capture.")
        if self.outcome == "amended" and not self.new_invariant_version:
            raise ValueError("new_invariant_version required when outcome == 'amended'.")
        return self


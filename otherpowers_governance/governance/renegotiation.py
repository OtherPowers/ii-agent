from __future__ import annotations

from typing import List, Optional, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


class RenegotiationIntent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contested_invariant: str
    triggering_event: str

    situated_context: Optional[str] = None

    impacted_groups: List[str] = Field(default_factory=list)
    harm_claim: str
    counter_harm_risk: str

    non_negotiables: List[str] = Field(default_factory=list)
    alternatives_considered: List[str] = Field(default_factory=list)

    submitted_by: str

    @field_validator(
        "contested_invariant",
        "triggering_event",
        "harm_claim",
        "counter_harm_risk",
        "submitted_by",
    )
    @classmethod
    def _strip_required_strings(cls, v: str) -> str:
        return (v or "").strip()

    @field_validator("impacted_groups", "non_negotiables", "alternatives_considered")
    @classmethod
    def _strip_list_items(cls, v: List[str]) -> List[str]:
        return [(s or "").strip() for s in (v or []) if (s or "").strip()]

    @model_validator(mode="after")
    def _enforce_minimum_viable_intent(self) -> "RenegotiationIntent":
        if not self.impacted_groups:
            raise ValueError("impacted_groups must not be empty")

        if not self.harm_claim:
            raise ValueError("harm_claim must not be empty")

        if not self.counter_harm_risk:
            raise ValueError("counter_harm_risk must not be empty")

        if not self.non_negotiables:
            raise ValueError("non_negotiables must not be empty")

        if not self.alternatives_considered:
            raise ValueError("alternatives_considered must not be empty")

        # submitter must be namespaced (collective:, org:, role:, etc.)
        if ":" not in self.submitted_by:
            raise ValueError("submitted_by must be namespaced (e.g., collective:stewards)")

        return self


class RenegotiationResolution(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contested_invariant: str

    outcome: Optional[str] = None
    summary: Optional[str] = None
    community_window_closed: bool = False

    # tolerate historical + newer test shapes
    alt_modality_trace: Union[str, List[str], None] = ""

    quorum_attestations: List[str] = Field(default_factory=list)

    # optional evolution marker referenced by tests
    new_invariant_version: Optional[str] = None

    @field_validator("contested_invariant")
    @classmethod
    def _strip_invariant(cls, v: str) -> str:
        return (v or "").strip()

    @field_validator("quorum_attestations")
    @classmethod
    def _strip_attestations(cls, v: List[str]) -> List[str]:
        return [(s or "").strip() for s in (v or []) if (s or "").strip()]

    @field_validator("alt_modality_trace", mode="before")
    @classmethod
    def _normalize_alt_trace(cls, v):
        if v is None:
            return ""
        if isinstance(v, list):
            cleaned = [(s or "").strip() for s in v if (s or "").strip()]
            return "; ".join(cleaned)
        if isinstance(v, str):
            return v.strip()
        return v


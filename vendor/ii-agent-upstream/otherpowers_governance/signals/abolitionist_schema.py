from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Tuple

from pydantic import BaseModel, Field, ConfigDict, model_validator


class DissolutionMode(str, Enum):
    """Right to Dissolution: hard-halt is a first-class safety outcome."""
    NONE = "none"
    SOFT_HALT = "soft_halt"   # stop emitting; keep local diagnostics
    HARD_HALT = "hard_halt"   # stop processing; require manual renegotiation
    DECOMPOSE = "decompose"   # destroy/rotate keys, disable pipelines, revoke emitters


class ChannelKind(str, Enum):
    """Accessibility + Temporal Plurality: channels can be low-bandwidth by design."""
    API = "api"
    FILE_DROP = "file_drop"
    HUMAN_FORM = "human_form"
    SMS = "sms"
    RADIO = "radio"
    OFFLINE = "offline"
    OTHER = "other"


class ContestationPath(str, Enum):
    """Contestability: paths for affected subjects/community to challenge emissions."""
    COMMUNITY_REVIEW = "community_review"
    SUBJECT_APPEAL = "subject_appeal"
    INDEPENDENT_AUDIT = "independent_audit"
    LEGAL_AID = "legal_aid"
    OTHER = "other"


class Lineage(BaseModel):
    """
    Legibility of Lineage (Haraway): signals are always cooked.
    This is the context anchor that prevents 'view from nowhere' universalization.
    """
    model_config = ConfigDict(extra="forbid")

    origin_system: str = Field(..., min_length=1)
    data_sources: List[str] = Field(default_factory=list)  # e.g., dataset IDs, docs, sensors
    labor_context: Optional[str] = Field(default=None)      # who labeled / maintained / cleaned
    jurisdiction: Optional[str] = Field(default=None)       # legal/geo constraints
    metadata_context_hash: str = Field(..., min_length=16)  # non-null; stable reference


class TemporalEnvelope(BaseModel):
    """
    Temporal Plurality (Wong): no standardized time tyranny.
    The system must not treat lateness/out-of-sequence as invalidity.
    """
    model_config = ConfigDict(extra="forbid")

    observed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    received_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    channel: ChannelKind = ChannelKind.API

    # "Crip time" support: allow explicitly asynchronous validation without timeout penalties.
    async_validity: bool = True
    human_in_loop_required: bool = False
    # If human validation is required, do NOT enforce strict deadlines in core validation.
    # Deadlines can exist, but missing them must not auto-fail vulnerable-centered review.
    suggested_review_by: Optional[datetime] = None


class ReceiptOfLogic(BaseModel):
    """
    Contestability (Wells): when we do act, we leave a usable trace.
    This is not surveillance logging; it is a receipt intended for the harmed/affected.
    """
    model_config = ConfigDict(extra="forbid")

    plain_language_summary: str = Field(..., min_length=1)
    key_invariants_applied: List[str] = Field(default_factory=list)  # e.g., ["anti_enclosure", "withhold_on_carceral"]
    what_was_withheld_and_why: Optional[str] = None
    what_was_emitted_and_why: Optional[str] = None

    # Designed for margins: accessible formatting hooks.
    accessibility_notes: Optional[str] = None
    translation_available: bool = False

    contestation_paths: List[ContestationPath] = Field(default_factory=lambda: [ContestationPath.COMMUNITY_REVIEW])


class CaptureRisk(BaseModel):
    """
    Anti-Enclosure (Mostaque/edge): resist platform paternalism & capture.
    """
    model_config = ConfigDict(extra="forbid")

    must_run_locally_capable: bool = True   # can be executed without a single vendor API
    api_gating_detected: bool = False       # if true -> escalate
    proprietary_lock_in_detected: bool = False
    single_entity_control_risk: Optional[str] = None  # narrative risk statement


class HarmDetection(BaseModel):
    """
    Harm-aware buffer: if carceral patterns are detected, default to withhold=True.
    """
    model_config = ConfigDict(extra="forbid")

    carceral_pattern_match: bool = False
    patterns: List[str] = Field(default_factory=list)  # e.g., ["naming_shaming", "surveillance_inference"]
    vulnerable_groups_implicated: List[str] = Field(default_factory=list)  # do NOT require identity; can be category-level
    recommended_withhold: bool = False


class AbolitionistSignal(BaseModel):
    """
    A signal record that is valid only if it can be:
    - situated (lineage),
    - accessible across time,
    - contestable,
    - decomposable (right to dissolution),
    - resistant to enclosure/capture,
    - harm-buffered against carceral drift.
    """
    model_config = ConfigDict(extra="forbid")

    # Minimal "what":
    kind: str = Field(..., min_length=1)
    payload: Dict[str, Any] = Field(default_factory=dict)

    # Core abolitionist fields:
    lineage: Lineage
    temporal: TemporalEnvelope = Field(default_factory=TemporalEnvelope)
    receipt: ReceiptOfLogic

    capture_risk: CaptureRisk = Field(default_factory=CaptureRisk)
    harm_detection: HarmDetection = Field(default_factory=HarmDetection)

    # Control plane outcomes:
    withhold: bool = False
    dissolution: DissolutionMode = DissolutionMode.NONE

    # Non-coercive governance note: if hierarchy reinforcement detected, halt for renegotiation.
    renegotiation_required: bool = False

    @model_validator(mode="after")
    def enforce_abolitionist_invariants(self) -> "AbolitionistSignal":
        # Invariant 9: lineage must be legible and context hash must not be null.
        if not self.lineage.metadata_context_hash or self.lineage.metadata_context_hash.strip() == "":
            raise ValueError("Invariant violation: metadata_context_hash cannot be null/blank (Legibility of Lineage).")

        # Harm-aware buffer: carceral patterns -> withhold must be true.
        if self.harm_detection.carceral_pattern_match:
            self.withhold = True
            # Ensure receipt states what was withheld.
            if not self.receipt.what_was_withheld_and_why:
                self.receipt.what_was_withheld_and_why = (
                    "Withheld due to detected carceral pattern(s): "
                    + ", ".join(self.harm_detection.patterns or ["unspecified"])
                )
            # Mark renegotiation if vulnerable groups are implicated.
            if self.harm_detection.vulnerable_groups_implicated:
                self.renegotiation_required = True

        # Anti-enclosure: capture indicators should trigger at least soft-halt or renegotiation.
        if self.capture_risk.api_gating_detected or self.capture_risk.proprietary_lock_in_detected:
            self.renegotiation_required = True
            if self.dissolution == DissolutionMode.NONE:
                self.dissolution = DissolutionMode.SOFT_HALT

        # Contestability: emissions must carry a human-readable receipt.
        if not self.receipt.plain_language_summary.strip():
            raise ValueError("Invariant violation: receipt.plain_language_summary required (Contestability).")

        # Right to dissolution: if renegotiation required AND we are still emitting, prefer halt.
        if self.renegotiation_required and not self.withhold:
            # Not an absolute rule, but a strong default: when in doubt, stop emitting.
            self.withhold = True
            if self.dissolution == DissolutionMode.NONE:
                self.dissolution = DissolutionMode.SOFT_HALT
            if not self.receipt.what_was_withheld_and_why:
                self.receipt.what_was_withheld_and_why = (
                    "Withheld pending renegotiation (Proactive Reparation / Anti-Enclosure safeguard)."
                )

        return self


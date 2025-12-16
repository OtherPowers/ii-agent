# /Users/bush3000/ii-agent-reorg/otherpowers_governance/intelligence/posture_reasoning.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class PostureReasoning:
    """
    Human/agent legibility for posture.

    Constraints:
    - No identities
    - No sources
    - No topics
    - No “who did what”
    - Only condition-language and suggested stance posture
    """

    def explain_posture_string(self, posture: str) -> Dict[str, object]:
        p = (posture or "neutral").strip().lower()

        if p == "neutral":
            return {
                "posture": "neutral",
                "summary": "Conditions appear stable with no immediate need for adjustment.",
                "signals": ["no dominant risk patterns detected"],
            }

        if p == "increase_care":
            return {
                "posture": "increase_care",
                "summary": "Signals suggest rising sensitivity; increase care and reduce unnecessary reach.",
                "signals": ["early pressure patterns", "moderate volatility", "prefer slower changes"],
            }

        if p == "high_care":
            return {
                "posture": "high_care",
                "summary": "Conditions indicate elevated fragility; prioritize restraint, consent checks, and lower-risk paths.",
                "signals": ["sustained pressure", "low plurality signals", "heightened uncertainty possible"],
            }

        # Unknown posture stays legible and non-judgmental.
        return {
            "posture": p,
            "summary": "Posture is unclassified; default to restraint and minimal assumptions.",
            "signals": ["unclassified posture", "prefer conservative defaults"],
        }


# Creative Intelligence Invariants (OtherPowers.co)

This document freezes the non-negotiable invariants of the Creative Intelligence layer.
These are not implementation details. They are *constraints on possibility*.

## 1. Silence Is a First-Class Outcome
Silence is not failure, absence, or error.
Silence is an intentional, valid state that must:
- propagate without mutation
- never trigger emission
- never be coerced into output

Any component that converts silence into signal is invalid.

## 2. No Hierarchy, No Ranking, No Scoring
The system must never:
- score
- rank
- order
- compare
- optimize toward a single axis

There is no “best” signal.
There is no “stronger” signal.
There is no “confidence” scalar.

All meaning is contextual, relational, and non-comparable.

## 3. Emission Is Edge-Triggered, Not Volume-Triggered
Signals emit at most once per lifecycle boundary.
Repeated inputs must not amplify output.

This prevents:
- feedback inflation
- persuasion dynamics
- covert optimization loops

## 4. Public Surface Is Minimal by Design
The ONLY supported public construction surface is:

- `new_signal(...)`

Everything else is:
- internal
- private
- non-stable
- non-importable from the package root

This prevents accidental coupling and semantic drift.

## 5. Accumulation ≠ Evaluation
Accumulators may:
- remember posture
- preserve state
- track continuity

Accumulators may NOT:
- judge
- select
- prefer
- discard based on value

Memory is not evaluation.

## 6. Routing Preserves Identity
Routers may:
- pass signals forward
- block signals
- respect silence

Routers may NOT:
- transform meaning
- inject metadata
- annotate importance

Routing is transport, not interpretation.

## 7. Governance Is Non-Coercive
Governance decisions:
- never force output
- never override silence
- never escalate authority

Governance may withhold.
Governance may defer.
Governance may remain undecided indefinitely.

## 8. Extension Requires Renegotiation
Any attempt to add:
- metrics
- probabilities
- weights
- optimization targets
- learning signals

requires explicit renegotiation of these invariants.

Silent drift is considered a failure mode.

---

**Status:** Frozen  
**Change Policy:** Explicit renegotiation only  
**Audience:** Future maintainers, auditors, co-builders, and non-human intelligences


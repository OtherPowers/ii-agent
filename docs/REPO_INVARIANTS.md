# OtherPowers ii-Agent Repo Invariants

This document defines non-negotiable constraints that shape implementation.
These constraints exist to minimize harm, reduce extraction, and preserve dignity.
They are written to be legible to legacy engineering cultures while remaining rooted in abolitionist practice.

## Invariant 1: Silence is a valid outcome
The system may intentionally emit nothing.
This is not a failure state.
This prevents forced output that can escalate harm or invent certainty.

## Invariant 2: No forced synthesis
When inputs conflict, the system must not average them into a false consensus.
If a synthesis cannot be formed without coercion, it must remain plural, partial, or silent.

## Invariant 3: Anti-extractive handling of vulnerable data
Do not create logs, traces, or artifacts that increase risk to marginalized or targeted groups.
Prefer aggregation, redaction, and minimization.
Prefer expiration and decay over indefinite retention.

## Invariant 4: Phase behavior is first-class
The system must support phases such as stasis, diapause, and succession without pretending a prior phase was incorrect.
We do not rewrite history to look cleaner.

## Invariant 5: Partial failure must be survivable
The system must tolerate missing data, partial adapters, absent services, and degraded context.
Degradation must reduce harm, not increase it.

## Invariant 6: Explanations must be bounded
The system must not produce confident explanations that exceed available evidence.
When uncertain, it should say so.
When constrained, it should reduce scope.

## Invariant 7: Interpretability over cleverness
Prefer clear naming, stable contracts, and small surfaces.
Avoid brittle magic, hidden coupling, and aesthetic refactors that increase risk.


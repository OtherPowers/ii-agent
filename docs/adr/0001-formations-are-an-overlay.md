# ADR 0001: Formations are an overlay, not a folder structure

## Status
Accepted

## Context
We expanded the conceptual primitives of the system into a richer set of formations.
We must preserve existing repository structure and naming because:
- it is already public and accountable,
- it is legible to legacy engineering systems,
- it reduces risk and churn,
- it prevents rewrite spirals that erase lineage.

## Decision
We represent the expanded formations as a minimal semantic overlay.
This overlay:
- lives in a small, importable registry,
- does not require renaming modules or moving files,
- can be referenced by existing components without altering their contracts.

## Consequences
- We can evolve meaning without destabilizing the runtime.
- We can gradually integrate formation-aware behavior where it is useful.
- Contributors can learn the system without navigating a new taxonomy.
- We can later add tests that enforce repo invariants without restructuring the codebase.


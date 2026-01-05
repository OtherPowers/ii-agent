# ADR 003: Append-Only Lineage as Harm-Reduction Memory

## Status
Accepted

## Context
Many technical systems treat memory as something to optimize, compress, or overwrite. This often leads to erasure of context, loss of accountability, and the quiet removal of traces that would otherwise signal harm, drift, or unresolved impact.

These patterns disproportionately harm marginalized communities by making it difficult to surface how decisions were made, what was refused, and why certain paths were closed.

OtherPowers rejects overwrite-oriented memory.

## Orientation
Append-only lineage describes how the system remembers without extracting, summarizing away, or retroactively correcting its own history.

Memory here is not surveillance.
It is not analytics.
It is not optimization input.

It is lineage.

Lineage preserves sequence without interpretation. It allows the system to acknowledge what occurred without reifying identities, ranking events, or enforcing narrative closure.

## Decision
We design memory surfaces to be append-only.

This is expressed through:
- VITALS and similar records that only grow
- refusal to overwrite or “clean up” prior entries
- tolerance for partial, minimal, or ambiguous traces
- survival under read-only or unavailable storage
- avoidance of identity-bearing or extractive detail

Append-only memory prioritizes continuity over clarity and safety over completeness.

## Consequences
- Memory may be messy, incomplete, or unresolved.
- Older entries are not reinterpreted to fit newer understanding.
- Lineage may reflect pauses, refusals, or long periods of inactivity.
- The system can continue functioning even when memory cannot be written.

These outcomes are intentional.
They prevent retroactive harm and preserve the possibility of collective review without coercion.

## Notes
Future contributors may attempt to introduce pruning, summarization, or replacement in the name of performance or cleanliness.

This ADR exists to make clear that such changes risk reintroducing extractive memory practices and are incompatible with this system’s orientation.


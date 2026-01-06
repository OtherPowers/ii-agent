# Field Boundary v1

Status: **Frozen**
Scope: `tending/pulse.py` public emission surface

## Guarantees
- Deterministic stdout under identical conditions
- Locale, timezone, and environment independent
- Append-only side effects (VITALS.md)
- Silence under override pressure
- Order-stable, line-stable emission

## Contract
The following stdout lines are **public surface**:
1. `field pulse active`
2. `seasons present: <ordered list>`
3. `diurnal phase: <value>`

No additional stdout lines may be added without:
- an explicit version bump
- updated vows
- new contract tests

## Rationale
Field emission is a **witness surface**, not a logging channel.
Expansion without consent is a form of harm.

## Authority
This boundary is enforced by tests, not convention.

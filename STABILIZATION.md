# Stabilization Checkpoint

Status: GREEN  
Date: 2026-01-07  
Owner: OtherPowers ii-Agent

This document marks a known-good stabilization point in the ii-Agent codebase.
At this state, all surface, pulse, lattice, and vitals contracts are passing
under full test execution.

This checkpoint exists to prevent semantic drift, accidental expansion,
or “helpful” refactors that violate restraint-based design principles.

---

## Frozen Surfaces

The following components are considered behaviorally frozen at this checkpoint:

- `tending.pulse`
- `tending.field_state`
- `tending.sensing_lattice`

Frozen means:
- Public behavior must not change without explicit contract revision
- Tests are enforcement, not suggestion
- Silence is an intentional outcome, not an error

---

## Guaranteed Properties

At this checkpoint, the system guarantees:

### Execution
- `python -m tending.pulse` always exits with code `0`
- Runs cleanly from empty directories
- Runs cleanly with missing or read-only `VITALS.md`
- Tolerates minimal or absent environment configuration

### Surface Behavior
- Emits minimal, ordered stdout when not refracted
- Emits silence under override pressure
- Never emits stderr
- Never escalates output across identical runs
- Idempotent across directories and invocations

### Schema Discipline
- Field surface schema is minimal and order-locked
- No analytic, behavioral, or identity leakage
- No inference, ranking, or optimization
- Seasons and diurnal states may coexist without forcing linear narrative

### Care Invariants
- Protection is achieved through restraint, not enforcement
- Silence is a valid and successful outcome
- Cooldown and opacity are treated as care, not failure

---

## Non-Goals (Explicit)

This system does NOT:
- Optimize for usefulness
- Infer intent
- Expand meaning
- Log internal pressure
- Escalate signals
- Act as a security boundary

Any change that introduces the above requires an explicit contract break
and a new stabilization checkpoint.

---

## Change Control

If tests fail after this point:
1. Assume the code is correct
2. Investigate the change, not the symptom
3. Do not “fix forward” without understanding the violated invariant

This file is the memory of “green.”


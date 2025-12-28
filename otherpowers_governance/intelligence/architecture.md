# Influence Spine — Architectural Boundaries

This document defines the allowed behaviors, constraints, and invariants
of the Influence Spine and its adapters within the OtherPowers governance lineage.

It is descriptive, not aspirational.
It exists to prevent ambiguity, drift, and accidental coercion.

---

## Role

The Influence Spine is a **translator**, not a decider.

It accepts contextual signals,
interprets them through a bounded interface,
and may propose influence *only when governance allows*.

It does not:
- evaluate worth
- rank entities
- enforce outcomes
- optimize behavior
- guarantee output

---

## Core Invariants

### 1. Silence Propagation

If upstream context produces silence,
the Influence Spine **must return `None`**.

No bridge instantiation.
No emission attempt.
No mutation.

Silence is a first-class outcome.

---

### 2. Lazy Emission

Emission infrastructure **must not exist** unless:
- upstream context is non-silent, and
- governance has not refused participation

The bridge is created *only when needed*.

---

### 3. Governance Refusal Is Terminal

If governance refuses emission:
- the adapter returns `None`
- no retries occur
- no fallback paths are invoked

Refusal is not an error condition.
It is a valid and complete result.

---

### 4. No Phantom Side Effects

The Influence Spine may not:
- mutate input context
- create hidden state
- emit signals implicitly
- leak partial artifacts

All influence must be explicit, bounded, and traceable.

---

### 5. Adapter Is Replaceable

The Influence Spine Adapter:
- is swappable
- holds no authority
- contains no domain logic
- must tolerate being bypassed

Its legitimacy comes from restraint, not reach.

---

## Forbidden Behaviors

The Influence Spine must never:

- coerce downstream systems
- manufacture consent
- collapse choice through inevitability
- emit influence when silence is present
- infer permission from absence of refusal

---

## Testing Contract

These invariants are enforced via smoke tests that assert:

- silence → `None`
- no bridge creation on silence
- no emission on refusal
- exactly-once emission when permitted

Any change that violates these tests
is considered a regression in legitimacy.

---

## Evolution

This architecture is intentionally incomplete.

Future extensions must:
- preserve silence semantics
- maintain refusal as terminal
- avoid coupling influence to authority

If an extension cannot meet these constraints,
it does not belong in the Influence Spine.


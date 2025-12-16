# Invariants

These properties are intentionally stable.  
They may evolve only with explicit, documented intent.

## Scope
- Core behavior lives in `field_attunement/` and `otherpowers_governance/signals/`
- Public surface is limited to `otherpowers_governance/__init__.py`

## Data & Identity
- No identity persistence
- No user profiling
- No attribution, ranking, or reputation
- No logs beyond local, overwrite-only field artifacts

## Silence
- Silence is a valid and meaningful outcome
- Silence may return empty or decay
- Absence of signal must never raise errors

## Fields
- Field artifacts are local-only
- Field writes are overwrite-only
- Missing or malformed field data must fail softly (`{}`)

## Execution
- No network I/O in core paths
- No background daemons or schedulers
- No global registries or central authorities

## Failure Semantics
- No exceptions escape the public boundary
- Invalid inputs are ignored or coerced, not rejected
- System must remain usable in degraded states


# zz_MISC_CANDIDATES

This file marks areas for **future cleanup review**.
Nothing listed here is safe to delete without re-verification.

## Categories

### 1. Historical / Archive Candidates
- scripts/_archive/
- vendor/ii-agent-upstream/
- zz_misc/
- otherpowers_governance/signals/_legacy/

### 2. Duplicate / Shadow Trees
- field_attunement/ vs otherpowers_governance/signals/_legacy/field_attunement/
- zz_misc/zz_field_attunement/

### 3. Template Libraries (intentionally kept)
- .templates/** (do not prune without explicit intent)

### 4. DS_Store Noise
- Safe to remove later via scripted sweep

## Rule
No deletion without:
- a test proving non-reachability
- or an explicit archival move (not rm)

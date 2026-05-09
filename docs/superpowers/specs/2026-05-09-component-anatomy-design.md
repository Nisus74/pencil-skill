# Design spec: component anatomy — reading and using components from .pen files

**Date:** 2026-05-09
**Status:** Implemented (v1.6.0)

---

## Problem

The pencil-dev skill handles component *discovery* (inventory via `batch_get`) and *decision logic* (use existing vs. build from scratch) well. However, once a component is found, the skill provides no guidance on how to read its internal structure before using it.

Specific gaps:

| Gap | Impact |
|-----|--------|
| No "inspect before use" step | AI guesses descendant keys; ops fail with unknown-key errors |
| Slots defined in schema but never demonstrated in practice | AI doesn't know to set `children: [...]` on a slot id |
| Nested `/` path syntax mentioned once, never explained | AI uses top-level key that doesn't exist, breaks instantiation |
| Component states not covered | AI can't put a component into loading/disabled/error state |

---

## Solution

Three coordinated artifacts following the existing architecture (SKILL.md = concise, `references/` = deep, `assets/examples/` = worked):

### 1. SKILL.md patch

Added "Reading an unfamiliar component" subsection inside the "Components first" block, after the two inventory scans and before the decision logic. Introduces `batch_get({ nodeIds: [...], readDepth: 4 })` as a mandatory step for unfamiliar components, explains what to look for, and points to the reference file and example.

### 2. `references/component-anatomy.md` (new, ~250 lines)

Five sections:
- **Reading a component's structure** — the `readDepth: 4` call, a field-by-field guide to the response, and the mental scan order
- **Identifying and filling slots** — what `slot: [...]` means in JSON, how to fill via `descendants.slotId.children`
- **Mapping descendant keys** — direct ids, nested `/` paths, what three things a descendant entry can do, plus a worked trace of a three-level tree
- **Discoverable properties** — valid overrides by node type, top-level ref vs. descendants distinction
- **Component states in instances** — reading `theme` to discover states, setting state on a ref, caution about verifying from structure

### 3. `assets/examples/example-component-deep-dive.md` (new, ~150 lines)

Full worked scenario using a `CardPrimary` component for a product listing. Five steps:
1. Inventory scan
2. Deep read with annotated response
3. Mental map derived from the response
4. Three instantiation patterns (simple override / slot fill / nested path)
5. State variant (loading state)

---

## Gap coverage

| Gap | Fixed by |
|-----|---------|
| Reading structure before use | SKILL.md subsection + anatomy reference § Reading |
| Identifying slots | anatomy reference § Slots + example Pattern 2 |
| Nested `/` path syntax | anatomy reference § Descendant keys + example Pattern 3 |
| Component states | anatomy reference § States + example Step 5 |

---

## Verification

- `skill-lint.py` passes with 0 violations
- All 39 test suite tests pass
- Version bumped: `1.5.0` → `1.6.0`

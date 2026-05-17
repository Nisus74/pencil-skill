# Heuristics scoring

A structured way to evaluate a design against the established UX heuristics. Use this when the user asks for a critique, review, or audit of a `.pen` file; when the design is close-to-done and you want one pass over its UX qualities before declaring it shipped; or when comparing two design directions and need a defensible basis for the recommendation.

This reference sits next to [distinctiveness-checklist.md](distinctiveness-checklist.md), which is the *taste* pass. Heuristics scoring is the *UX* pass. Both run before declaring a design done; they answer different questions.

## When to run it
- The user said *"critique this"*, *"review the UX"*, *"audit this design"*, *"is this good?"*
- A design just landed at *"functionally done"* and you want a structured second look before handoff.
- Choosing between two directions and need a basis other than gut feeling.

When NOT to run it:
- Quick sketches and throwaway mocks; not worth the cycles.
- The user said *"go fast"*, *"ship it"*, *"don't polish"*.
- Mid-build; this runs once, near the end, not on every iteration.

## The ten heuristics

Adapted from Nielsen's heuristics, with the framing tuned for Pencil work.

### 1. Visibility of system status
The user knows what's happening. Loading states are explicit. Feedback follows action. Long operations show progress. The system never silently does or fails to do.

**Score 5:** Every action has feedback within 100–250ms; long operations show specific progress (*"Uploading 3 of 7"*); state changes are confirmed visibly.
**Score 3:** Most actions have feedback; some long operations show only a spinner.
**Score 1:** Actions feel disconnected; the user has to wonder whether they took effect.

### 2. Match between system and the real world
Language, concepts, and conventions follow the user's domain, not engineering's.

**Score 5:** Domain-specific terminology throughout; no system-jargon labels; metaphors and icons match user expectations.
**Score 3:** Mostly domain-aligned with one or two system-jargon leaks.
**Score 1:** Reads as a developer's model of the user's domain rather than the user's model.

See [ux-writing.md](ux-writing.md) for the copy patterns that drive this.

### 3. User control and freedom
The user can undo, cancel, or back out of any action. Destructive actions are reversible or have confirmation. The user owns their flow.

**Score 5:** Every destructive action is reversible or has a confirmation with specific consequence copy; back-stack works; the user never feels stuck.
**Score 3:** Most actions have escape routes; some destructive actions are immediate without confirmation.
**Score 1:** Destructive actions are unconfirmed; back navigation is broken or absent; the user can't recover from mistakes.

### 4. Consistency and standards
The design follows platform conventions and is internally consistent. Same things look the same; different things look different.

**Score 5:** Predictable patterns across the whole surface; reusable components are actually reused; visual language is coherent.
**Score 3:** Mostly consistent with a few one-off variations that read as accidental.
**Score 1:** Inconsistent vocabulary, mismatched button styles, components built from primitives where library components exist.

This score depends partly on the *"components-first"* discipline rule in SKILL.md.

### 5. Error prevention
The design prevents user errors before they happen. Constraints are visible; risky actions confirm before executing; defaults are sensible.

**Score 5:** Form constraints communicated up front (*"Workspace names must be lowercase, 3–32 characters"*); destructive actions show specific consequences; sensible defaults reduce the surface area for mistakes.
**Score 3:** Errors are mostly caught after submission; defaults are present but generic.
**Score 1:** Errors surface only after submission; defaults are absent or counter-intuitive.

### 6. Recognition over recall
Information needed for the task is visible; the user doesn't have to remember it from elsewhere.

**Score 5:** Context for any decision is visible at decision-time (a confirmation modal shows the items being deleted; a form shows the relevant prior values).
**Score 3:** Most decisions show context; some require memory of prior screens.
**Score 1:** The user has to hold information in their head across screens.

### 7. Flexibility and efficiency of use
The design serves both first-time users (clear, explicit) and frequent users (efficient, with shortcuts).

**Score 5:** Onboarding is clear; daily-use is efficient with shortcuts, bulk actions, command palettes, customisable workflows.
**Score 3:** First-use is clear; daily-use is functional without efficiency optimisations.
**Score 1:** Optimised for first-use only (every action explained), or for power users only (no onboarding).

### 8. Aesthetic and minimalist design
The design carries only what's needed. Decorative chrome, redundant copy, and visual flourishes that don't serve the task are absent or muted.

**Score 5:** Every element on the surface has a job; the design feels considered without being austere; visual hierarchy is clear.
**Score 3:** Mostly clean with some compounding-decoration moments (a heading with bold + colour + border + icon).
**Score 1:** Visually noisy; every element has multiple hierarchy signals; the eye doesn't know where to land.

The [distinctiveness-checklist.md](distinctiveness-checklist.md) catches the taste failures; this score covers the "too much chrome" UX failures.

### 9. Error recovery
When errors happen (and they will), recovery is clear and possible.

**Score 5:** Error messages are specific (what + why + how-to-fix per [ux-writing.md](ux-writing.md)); paths to recovery are obvious; data isn't lost; the user feels supported.
**Score 3:** Errors are explained; recovery is possible but requires user effort to find.
**Score 1:** Errors are generic (*"Something went wrong"*); recovery paths are unclear; user data is at risk.

### 10. Help and documentation
When the user needs help, it's available and useful.

**Score 5:** Inline help (tooltips, placeholder hints, contextual links) at the points where users actually need it; reference documentation is reachable from relevant surfaces.
**Score 3:** Help exists but is centralised in a docs section the user has to seek out.
**Score 1:** No inline help; documentation is absent or inaccessible from the surface.

## How to score

For each of the ten heuristics, walk the design and assign a score of 1–5. Be honest. A score of 3 means *"acceptable with reservations"*, not *"fine."*

For each score ≤3, write one specific issue and one specific fix:

| # | Heuristic | Score | Issue | Fix |
|---|---|:---:|---|---|
| 1 | System status | 5 | (none) | (none) |
| 2 | Real-world match | 3 | *"Workspace"* used in nav, *"team"* in settings, *"organisation"* in billing | Pick one term; rename across all three surfaces |
| 3 | User control | 4 | Delete action immediate without confirmation | Add confirmation modal with specific consequence: *"Delete the 'analytics-2025' workspace and all 234 designs"* |
| ... | ... | ... | ... | ... |

## Composite score

Sum the ten scores. Out of 50:

- **45–50:** Production-ready; minor polish only.
- **38–44:** Solid; fix the items scoring ≤3 before declaring done.
- **30–37:** Functional but rough; substantive work needed on the lowest-scoring heuristics.
- **<30:** Not yet ready; the design needs another iteration on UX fundamentals before polish makes sense.

Don't optimise for a high composite score by inflating ratings. The scoring's value is in surfacing real issues; a quietly-honest 38 is more useful than an inflated 47.

## Anti-patterns in heuristic scoring

- **Scoring every heuristic at 5 because it's *"basically fine"*.** Heuristic scoring's job is to surface the gaps; *"fine"* is usually 3 or 4.
- **Adding a heuristic of your own to inflate the count.** Ten heuristics, defined; don't drift.
- **Scoring without specific examples.** A score of 2 with no example is unactionable. Cite a specific element.
- **Mistaking the heuristics for taste rules.** Heuristic scoring is the UX pass; the [distinctiveness-checklist.md](distinctiveness-checklist.md) is the taste pass. Both run; they answer different questions.

## Pencil-specific

### Score against the populated state
A design with three rows in a table will score higher on every heuristic than the same design with three hundred. Score against realistic data volume, not the empty version. See [cognitive-load.md](cognitive-load.md) on the populated-state verification.

### Score under both modes if dark mode applies
Some heuristic failures show up only under one mode. A focus ring that scores well in light mode may be invisible in dark mode (failing heuristic 1). A semantic colour that scores well for error in light mode may be unreadable in dark mode (failing heuristic 9).

### Capture the scoring in `context` for handoff
When scoring a design that will be handed to engineering, write the scoring table into the design's top-level frame's `context` string. The engineer reading the file knows what UX issues the design author was aware of and which were intentional vs deferred.

### Re-score after fixing
After issuing a `batch_design` round of UX fixes, re-score the affected heuristics only. Don't re-score the ones that were already 5; trust the work.

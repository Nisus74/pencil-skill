# Distinctiveness checklist

A short rubric the agent runs *once* after the design is composed, before declaring done. The goal is to surface "this is still generic" issues that pass the discipline checks but read as AI-default to a designer's eye.

This isn't a polish loop. It runs **at most once**, with an explicit kill switch, so the live-iteration cadence stays intact.

## When this runs

- Step 6 of the SKILL.md default workflow, after compose and the section-end screenshot.
- Skips entirely if the user said *"go fast"*, *"ship it"*, *"don't polish"*, or otherwise signalled they want the design committed as-is.
- Runs once per design task. After one revision round, the loop exits regardless of remaining items.

## How to run it

1. Take the final screenshot of the design (whole page, not a subtree).
2. Walk the 9 questions below in order. For each, answer aloud: *yes (passes)*, *no (fails, propose one fix)*, or *not applicable (skip this one for this task)*.
3. If any item fails, propose ONE concrete fix per failed item, not a list, one fix that addresses the root issue. Apply the fixes in a single follow-up `batch_design` chunk.
4. Take a final post-revision screenshot. Stop. Hand back.

If 0 items fail: the design passed. Hand back without changes.

## The 9 questions

### 1. Aesthetic direction named in the plan

Did you state a specific aesthetic direction before building? If the plan says only "a SaaS dashboard" with no specific direction — no typography call, no density register, no surface treatment decision — the design is operating without intent and will default to the generic.

**Fail mode:** the plan is silent on aesthetic direction; the design landed in violet-on-white balanced-SaaS shell.
**Fix:** name the direction now (post-hoc): *"dense data product, hairline borders, no shadows, mono numerals."* Also name one reference brand, designer, or publication the direction maps to: *"reads like a Stripe internal tool"*, *"reads like the FT's data graphics"*, *"reads like Plain's settings UI"*. Adjective-only directions slide back into generic; a named reference anchors the call. Check if the design already contradicts the direction and propose specific revisions.

### 2. Accent used in a non-obvious place

Is the accent applied somewhere that isn't *every primary CTA, every active state, every link*? If the accent appears in 12 places across the screen with the same weight, it stops being an accent.

**Fail mode:** accent on CTA + active sidebar item + KPI deltas + chart bars + link colour + badges + sparklines, all at full saturation.
**Fix:** strip the accent from at least 2 of those places. Make it earn its presence in fewer locations with more impact.

### 3. Typography shows personality, not just hierarchy

Beyond size and weight, is there a typographic *choice* that's visible? Type pairing, mono numerals where they help, small caps on a label, deliberate tracking?

**Fail mode:** the same font everywhere with H1/H2/Body/Small as the only differentiation. Nothing the eye remembers.
**Fix:** introduce one typographic move. Mono numerals on data, small caps on section labels, or a deliberate weight contrast that goes beyond the obvious.

### 4. At least one density choice is deliberate

Did you make a density call (airy, balanced, dense) and apply it consistently in one region? Or did the whole design land in default-balanced because no decision was made?

**Fail mode:** every region uses the same 16/24/32 spacing rhythm; nothing reads as denser-than-default or airier-than-default.
**Fix:** pick one region and shift it. Tighten the table to dense (8/12 row padding) or open up the hero (96+ vertical padding). Density variance signals intent.

### 5. The page has a signature moment

Is there one moment on the page that wouldn't survive being deleted? A custom data visualisation, a specific type move on a hero, a deliberate empty state, an element that gives the page identity beyond competent layout.

**Fail mode:** every region is competently generic; nothing on the page would be missed.
**Fix:** invest in one element. Make the chart specific, give the empty state real character, redesign one card to do something the others don't.

### 6. AI-default tells are absent

Does the design have any of the anti-patterns from the Aesthetic foundation section — pure white/black, Inter with no direction, pill badges defaulted to `cornerRadius: 999`, full-opacity accent everywhere, soft shadows where the direction called for hairline borders?

**Fail mode:** the design reads as AI-generated at a glance — not because of any single flaw, but because nothing signals deliberate intent.
**Fix:** name the specific tell and override it. "Cards have soft shadows but the direction called for flat surfaces. `Update(cardId, { effect: [] })`."

### 7. Microcopy feels specific to this product

Does the copy feel like it belongs to this product, or is it generic SaaS placeholder text?

**Fail mode:** *"How your product performed over the last 7 days."* *"Something went wrong. Please try again."* *"No items found."* All interchangeable with any other SaaS product.
**Fix:** rewrite 1–3 microcopy strings to be specific to the product's domain. "API calls this week" not "Activity over the last 7 days." "Connection lost — retry now" not "Something went wrong."

### 8. Surface treatment matches the stated direction

Does the chrome (borders vs shadows, corner radii, surface hierarchy, light vs dark mode) match the aesthetic direction stated in the plan? AI defaults drift toward soft shadows + medium radius + medium hierarchy regardless of what was asked for.

**Fail mode:** direction called for a dense data product with hairline borders, but every card has a soft shadow and `cornerRadius: 12`.
**Fix:** swap the chrome to match the direction. Remove shadows where the direction didn't call for them. Tighten radii for utilitarian surfaces.

### 9. Category-reflex test (two-tier)

This is the sharpest single distinctiveness check. Run both tiers; if either is obvious, the design hasn't escaped training-data gravity.

**First-order:** could someone guess the theme and palette from the product category alone?
- Observability → dark blue
- Healthcare → white plus teal
- Fintech → navy plus gold
- Crypto → neon on black
- AI product → off-white plus violet or orange
- Developer tool → dark mono on black

If the answer is *"yes, obviously"*, the design is operating from the first reflex tier.

**Second-order:** could someone guess the aesthetic family from the category plus the anti-references the user named?
- *"AI workflow tool that's not SaaS-cream"* → editorial-typographic
- *"Fintech that's not navy-and-gold"* → terminal-native dark mode
- *"Healthcare that's not white-and-teal"* → editorial photo-led
- *"Developer tool that's not Linear-dark"* → maximalist colour

If this second answer is obvious too, the design avoided the first reflex but landed in the second.

**Fail mode:** the design's direction *"AI workflow tool, modern, clean"* produced a violet-on-cream layout indistinguishable from the rest of the category. Or the direction *"AI workflow tool, but not the SaaS-cream default"* produced an editorial serif on warm-grey that's now itself the next-tier default.
**Fix:** rework the aesthetic direction until both tiers fail. Name what specifically would surprise someone who knows the category AND the anti-reference. Reach further from the reflex. The reflex-reject aesthetic lanes in [brand.md](brand.md) catch the currently-saturated second-tier families.

## Kill switch

The pass exits immediately if any of these are true:

- The user said *"go fast"*, *"ship it"*, *"don't polish"*, *"this is good enough"*, or any equivalent phrase at any point in the session.
- One revision round has already been applied and the user hasn't asked for more.
- The design has already had ≥3 iterations on the same area; further passes are unlikely to converge.

When the kill switch fires, hand back the design as-is. Do not present remaining checklist items as a TODO list, that's noise. The user opted out for a reason.

## What this isn't

- Not an accessibility check (those run in step 6 of SKILL.md and are non-negotiable).
- Not a polish loop (one round, then stop).
- Not a critique of the user's brief (if the user wanted violet-on-white, that's their call; the checklist asks whether the *agent* defaulted there without intent).
- Not a substitute for live iteration (the screenshot loop in step 5 is the main quality mechanism; this checklist catches what the loop missed because the agent was deciding while building).

## Worked example

A SaaS analytics dashboard built without stating an aesthetic direction:

| # | Question | Result |
|---|---|---|
| 1 | Aesthetic direction named? | **Fail.** The plan said "SaaS analytics dashboard"; no direction stated. The design defaulted. |
| 2 | Accent in non-obvious place? | **Fail.** Violet appears in 7+ places — CTA, sidebar active, KPI deltas, sparklines, brand mark, links, badges. |
| 3 | Typography shows personality? | **Fail.** Same proportional font throughout, no mono on data, no deliberate typographic move. |
| 4 | Deliberate density choice? | **N/A.** Balanced throughout; no region intentionally denser or airier. |
| 5 | Signature moment? | **Fail.** Nothing on the page would be missed if removed. |
| 6 | AI-default tells absent? | **Fail.** Soft shadows on every card. Pill badges. Blue default primary. |
| 7 | Microcopy product-specific? | **Fail.** *"How your product performed over the last 7 days"* — interchangeable with any SaaS. |
| 8 | Surface treatment matches direction? | **N/A.** No direction was stated. |
| 9 | Category-reflex test (both tiers)? | **Fail.** *"SaaS analytics dashboard"* → violet-on-white is the first-tier reflex; the design landed exactly there. Second tier doesn't apply because no anti-reference was named to escape from. |

Fail count: 6. The design is competent but undirected. Stating a direction in step 2 (*"dense data product: hairline borders, no shadows, mono on all numerals; reads like a Stripe internal tool, explicitly not the SaaS-violet default"*) and re-running the build against it would address all 6 fails.

This is exactly the gap this checklist is designed to catch.

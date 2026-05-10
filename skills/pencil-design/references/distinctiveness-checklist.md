# Distinctiveness checklist

A short rubric the agent runs *once* after the design is composed, before declaring done. The goal is to surface "this is still generic" issues that pass the discipline checks but read as AI-default to a designer's eye.

This isn't a polish loop. It runs **at most once**, with an explicit kill switch, so the live-iteration cadence stays intact.

## When this runs

- Step 5 of the SKILL.md default workflow, after compose and the section-end screenshot.
- Skips entirely if the user said *"go fast"*, *"ship it"*, *"don't polish"*, or otherwise signalled they want the design committed as-is.
- Runs once per design task. After one revision round, the loop exits regardless of remaining items.

## How to run it

1. Take the final screenshot of the design (whole page, not a subtree).
2. Walk the 8 questions below in order. For each, answer aloud: *yes (passes)*, *no (fails, propose one fix)*, or *not applicable (this archetype doesn't care)*.
3. If any item fails, propose ONE concrete fix per failed item, not a list, one fix that addresses the root issue. Apply the fixes in a single follow-up `batch_design` chunk.
4. Take a final post-revision screenshot. Stop. Hand back.

If 0 items fail: the design passed. Hand back without changes.

## The 8 questions

### 1. Aesthetic commitment named in the spec

Did you name the chosen archetype (or synthesised ephemeral) in your plan, before you started building? If the spec just says *"a SaaS dashboard"* with no archetype reference, the design is operating without aesthetic direction and will read as generic.

**Fail mode:** the spec is silent on aesthetic direction; the design defaults to violet-on-white SaaS shell.
**Fix:** name the archetype now (post-hoc), and if the design has drifted from it, propose the specific revisions to bring it in line.

### 2. Accent used in a non-obvious place

Is the accent applied somewhere that isn't *every primary CTA, every active state, every link*? If the accent appears in 12 places across the screen with the same weight, it stops being an accent.

**Fail mode:** accent on CTA + active sidebar item + KPI deltas + chart bars + link colour + badges + sparklines, all at full saturation.
**Fix:** strip the accent from at least 2 of those places. Make it earn its presence in fewer locations with more impact.

### 3. Typography shows personality, not just hierarchy

Beyond size and weight, is there a typographic *choice* that's visible? Type pairing, mono numerals where they help, small caps on a label, a serif accent in a heading, deliberate tracking?

**Fail mode:** Geist-everywhere with H1/H2/Body/Small as the only differentiation. Nothing the eye remembers.
**Fix:** introduce one typographic move. Mono numerals on data, small caps on section labels, or a single serif heading where the brand allows.

### 4. At least one density choice is deliberate

Did you make a density call (airy, balanced, dense) and apply it consistently in one region? Or did the whole design land in default-balanced because no decision was made?

**Fail mode:** every region uses the same 16/24/32 spacing rhythm; nothing reads as denser-than-default or airier-than-default.
**Fix:** pick one region and shift it. Tighten the table to mono-utility-dense (8/12 row padding) or open up the hero (96+ vertical padding). Density variance signals intent.

### 5. The page has a signature moment

Is there one moment on the page that wouldn't survive being deleted? A signature element, an inline data viz, a custom empty state, a microinteraction, a deliberate type pairing on a hero, that gives the page memorable identity.

**Fail mode:** every region is competently generic; nothing on the page would be missed.
**Fix:** invest in one element. Make the chart custom, give the empty state a real character (without illustrated mascots), redesign one card to do something the others don't.

### 6. Anti-cues from the chosen archetype are absent

Each archetype lists anti-cues, moves that break it. Walk them and confirm none appear in the design.

**Fail mode:** building in `analytics-dashboard` but the cards have shadows; building in `modern-pro-tool` but the active sidebar item is a coloured pill; building in `editorial-storytelling` but you added a comparison table.
**Fix:** remove the anti-cue. The archetype tells you the right replacement.

### 7. Microcopy carries the archetype's voice

Does the copy match the archetype's voice? Empty states, error messages, button labels, loading states, these are easy to leave as defaults and surprisingly powerful when shaped to the archetype.

**Fail mode:** *"Oh no! Something went wrong."* in a `modern-pro-tool` design (which calls for terse *"Couldn't load. Retry"*). Or *"Welcome to your dashboard! 🎉"* in an `analytics-dashboard` (which calls for confident, present-tense data framing).
**Fix:** rewrite 1–3 microcopy strings to match the archetype's voice section.

### 8. Surface treatment matches the archetype

Borders vs shadows, corner radii, surface hierarchy, dark vs light mode, does the design's chrome match what the archetype calls for? AI defaults often drift toward soft shadows + medium radius + medium hierarchy regardless of archetype.

**Fail mode:** building in `analytics-dashboard` (hairline borders, no shadows) but every card has a soft shadow. Building in `modern-pro-tool` (light mode canonical) but the design defaulted to dark.
**Fix:** swap the chrome to match. Borders for shadows, sharper radii, correct mode default.

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
- Not a substitute for live iteration (the screenshot loop in step 4 is the main quality mechanism; this checklist catches what the loop missed because the agent was deciding while building).

## Worked example: applying the checklist to today's `pencil-new.pen`

The SaaS analytics dashboard built earlier in the session, scored against the checklist:

| # | Question | Result |
|---|---|---|
| 1 | Archetype named in spec? | **Fail.** The spec said "SaaS analytics dashboard"; no archetype named. The design defaulted. |
| 2 | Accent in non-obvious place? | **Fail.** Violet appears in 7+ places (CTA, sidebar active, KPI deltas, sparklines, brand mark, link, "View all"). |
| 3 | Typography shows personality? | **Fail.** Inter throughout (which is also banned by SKILL.md), no mono on data, no small caps, no serif. |
| 4 | Deliberate density choice? | **Pass-ish.** Balanced throughout; no region intentionally denser or airier than default. |
| 5 | Signature moment? | **Fail.** Nothing on the page would be missed if removed. The mini-bar sparklines are the closest, but they're decorative, not functional. |
| 6 | Anti-cues absent? | **N/A.** No archetype was chosen. |
| 7 | Microcopy archetype-voiced? | **Fail.** Generic *"How your product performed over the last 7 days"* subhead; default to defaults. |
| 8 | Surface treatment matches archetype? | **N/A.** No archetype was chosen. |

Fail count: 5. The design is competent but undirected. Loading `analytics-dashboard` and re-running steps 4–5 of SKILL.md against that archetype would address all 5 fails.

This is exactly the gap this checklist is designed to catch.

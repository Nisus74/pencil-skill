# Impeccable-Style References Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Memory note `[[feedback_no_parallel_agents]]` rules out subagent-driven-development; everything runs inline.

**Goal:** Strengthen the Pencil design skill with eight new scaffold (verb) references and four enriched topic references, modelled on the structural template behind impeccable's bolder.md, quieter.md, and spatial-design.md. Result: agents iterating on the Pencil canvas have a richer vocabulary for *directional* refinement (bolder/quieter/distill/harden/polish/clarify/adapt/optimize) and deeper *topical* depth (layout, typography, colour, motion).

**Architecture:** Each scaffold ref follows the same template: opening framing → register split (brand vs product, citing brand.md and product.md) → assess current state (which Pencil MCP calls to make) → plan the refinement → apply across dimensions (typography, colour, layout, motion, copy) with concrete Pencil ops → NEVER list (specific anti-patterns) → verify quality (screenshot back) → handoff to polish.md. The four topic enrichments stay in their existing files; each adds a focused section of concrete rules absent from today's content.

**Tech Stack:** Markdown content authoring; Pencil MCP grammar (`batch_design`, `set_variables`, `get_screenshot`, `search_all_unique_properties`); existing references as cross-links.

---

## Authorial discipline (applies to every task)

These rules apply to every file written. Verify each before committing.

- **Voice match.** Use the established Pencil-design voice: italic-quoted example UX copy (*"Saved."*), register-aware framing, no em dashes (per `[[feedback_writing_style_mandatory]]`), AusE spelling (colour, behaviour, recognise, organised, centred), at least three distinct contractions, no binary contrasts (*"not X, but Y"*).
- **Pencil-flavoured, not impeccable-flavoured.** Each ref must reference at least one concrete Pencil MCP operation by name (`batch_design`, `set_variables`, `get_screenshot`, `replace_all_matching_properties`, etc). Drop CSS-specific examples from impeccable that don't apply to Pencil's node model.
- **Cross-links.** At least two existing references cross-linked per file (e.g. `[brand.md](brand.md)`, `[motion-design.md](motion-design.md)`).
- **Register split.** Every scaffold ref names how brand and product registers handle the direction differently. Cite `[brand.md](brand.md)` and `[product.md](product.md)`.
- **NEVER list.** Concrete, not abstract. *"Never use bouncy easing on UI controls"* not *"Never use bad animations"*. At least five items per scaffold ref.
- **Handoff.** Scaffold refs (except polish.md itself) end with: *"When the result feels right, hand off to [polish.md](polish.md) for the final pass."* polish.md instead closes the loop with verification against the original direction (step 2 of SKILL.md workflow).
- **Length target.** Scaffold refs: 150–250 lines. Topic enrichments: add 80–160 lines to an existing file.

---

## File structure

### New files (8 scaffold refs)
- Create: `skills/pencil-design/references/polish.md` — final alignment/spacing/consistency pass before shipping
- Create: `skills/pencil-design/references/bolder.md` — amplify safe designs without producing AI slop
- Create: `skills/pencil-design/references/quieter.md` — tone down loud designs without going generic
- Create: `skills/pencil-design/references/distill.md` — strip to essentials, remove unnecessary complexity
- Create: `skills/pencil-design/references/harden.md` — production-readiness (error states, edge cases, i18n, overflow)
- Create: `skills/pencil-design/references/clarify.md` — UX copy refinement (labels, errors, microcopy)
- Create: `skills/pencil-design/references/adapt.md` — cross-device adaptation (responsive, mobile, theming)
- Create: `skills/pencil-design/references/optimize.md` — performance and rendering improvements at handoff

### Modified files (4 topic enrichments + 1 SKILL.md wire-up)
- Modify: `skills/pencil-design/references/layout.md` — add hierarchy-through-multiple-dimensions table, "cards are not required" section, touch-target rules, optical adjustments
- Modify: `skills/pencil-design/references/typography.md` — add extreme weight pairing (900+200) section, monospace-as-accent discipline, condensed/extended widths
- Modify: `skills/pencil-design/references/color-and-contrast.md` — add "never gray on color" rule, dominant-color strategy (60% rule), gentler-contrast guidance
- Modify: `skills/pencil-design/references/motion-design.md` — add scroll-anchored reveal staggering (50–100ms), motion intensity reduction recipes
- Modify: `skills/pencil-design/SKILL.md` — add situational routing for new scaffold refs (lines 306–313 region) and add scaffold refs to Reference index (lines 414–432 region)

---

## Task ordering rationale

polish.md is built first because everything else hands off to it. Bolder/quieter follow as the discussed pair. Distill/harden and clarify/adapt pair next. Optimize is last among scaffolds (least Pencil-canvas-native; mostly hand-off advice). Topic enrichments follow scaffolds because the scaffold refs reveal which concrete rules need to land in the topic refs. SKILL.md wire-up is the closing task.

---

### Task 1: Author polish.md

**Files:**
- Create: `skills/pencil-design/references/polish.md`

**Section structure:**
1. Opening framing: polish is the final pass before shipping; not personality (that's delight.md), not directional refinement (that's bolder/quieter/distill). It's the alignment, spacing-consistency, and detail-coherence pass that catches the things that read as accidental.
2. Register split: brand polish leans on rhythm and atmosphere; product polish leans on alignment grids and token-consistency.
3. Assess current state: `get_screenshot` the full surface, run the squint test ([layout.md](layout.md)), check for rhythm breaks. Also `search_all_unique_properties` for any raw hex still in use.
4. Plan: pick one of three polish modes per surface (alignment-and-rhythm / token-and-consistency / detail-coherence). Don't try all three at once.
5. Apply across:
   - Alignment: ensure elements snap to the chosen grid; check optical centring on icons; verify text optical alignment at container edges (negative-margin trick from spatial-design.md).
   - Spacing: ensure 4pt scale discipline; replace any orphan values (22, 7, 33) with on-scale equivalents.
   - Token-consistency: every fill, border, font-family resolves to a variable, not a literal. Use `replace_all_matching_properties` to bulk-fix.
   - Detail-coherence: shadow depth scales consistent across components; border radii consistent within a component family; icon weights consistent.
   - Type rhythm: line-length under 75ch on body; light-on-dark line-height bump applied; tabular figures on numeric columns.
6. NEVER list: never call the design *polished* without re-running the screenshot loop; never polish before the direction is settled (you're polishing the wrong design); never let token-consistency become an excuse to skip the alignment pass; never add new ideas in the polish phase (that's a different pass); never declare done without checking both light and dark mode.
7. Verify quality: screenshot both modes; the surface should pass the squint test; no orphan spacing values remain; every colour, font, and motion duration resolves to a variable.
8. Closing: polish is the handoff target for the other scaffold refs. After polish, the design is ready for the SKILL.md step-6 completeness rubric.

**Cross-links:** `[layout.md](layout.md)`, `[typography.md](typography.md)`, `[color-and-contrast.md](color-and-contrast.md)`, `[delight.md](delight.md)`, `[distinctiveness-checklist.md](distinctiveness-checklist.md)`.

**Pencil ops referenced:** `get_screenshot`, `search_all_unique_properties`, `replace_all_matching_properties`, `set_variables`, `batch_design` (`U` ops for token migration).

- [ ] **Step 1: Draft polish.md against the section structure above**
- [ ] **Step 2: Verify the authorial discipline checklist (voice, AusE, no em dashes, three contractions, register split, two cross-links, five-item NEVER list)**
- [ ] **Step 3: Commit**

```bash
git add skills/pencil-design/references/polish.md
git commit -m "feat(skill): add polish reference for final shipping pass"
```

---

### Task 2: Author bolder.md

**Files:**
- Create: `skills/pencil-design/references/bolder.md`

**Section structure:**
1. Opening framing: *"bolder"* doesn't mean cyan/purple gradients, glassmorphism, neon-on-dark, or gradient text on metrics. It means stronger hierarchy, committed scale, decisive typography, and one sharper accent — applied with intent.
2. Register split: brand bolder = extreme scale, unexpected colour, typographic risk, committed POV; product bolder = stronger hierarchy, clearer weight contrast, one sharper accent, more committed density (not theatrics).
3. Assess current state: identify weakness sources (generic fonts, timid scale, low contrast, static, predictable). `get_screenshot` and squint-test for absent focal point.
4. Plan: pick the personality lane (maximalist / elegant drama / playful energy / dark moody); pick one hero moment per surface; decide risk budget.
5. Apply across dimensions:
   - Typography: swap generic fonts for distinctive ones (cite [typography.md](typography.md) reach-for list); extreme scale jumps (3x–5x, not 1.5x); weight contrast (900+200, not 600+400); reach for variable fonts and stylistic sets.
   - Colour: increase saturation but not to neon; pick one dominant colour to own 60% of the surface (committed strategy from [color-and-contrast.md](color-and-contrast.md)); avoid purple-to-blue gradient slop; use tinted neutrals harmonising with the dominant.
   - Spatial drama: 3x–5x scale jumps on hero elements; break the grid for hero moments; asymmetric layouts; generous space (96–192px gaps, not 24–48); intentional overlap.
   - Effects: dramatic shadows but not generic drop-shadows-on-rounded-rectangles; mesh / noise / geometric patterns for backgrounds; not glassmorphism.
   - Motion: staggered entrance choreography (200–300ms each with 100–150ms stagger, see [motion-design.md](motion-design.md)); scroll-triggered reveals; satisfying hover affordances; ease-out-quart/quint/expo (never bounce or elastic).
6. NEVER list: never reach for cyan/purple gradients; never glassmorphism as a default; never neon-on-dark as a shortcut; never gradient text on metrics or KPIs; never bouncy easing on UI controls; never make everything bold (then nothing is); never sacrifice readability for aesthetics.
7. Verify quality: AI slop test — if someone says *"AI made this bolder"* and it's believable, start over. Body text still readable; focal point is unambiguous; motion runs smoothly; passes accessibility.
8. Handoff to [polish.md](polish.md).

**Cross-links:** `[typography.md](typography.md)`, `[color-and-contrast.md](color-and-contrast.md)`, `[motion-design.md](motion-design.md)`, `[brand.md](brand.md)`, `[product.md](product.md)`.

**Pencil ops referenced:** `set_variables` (token re-declaration for new accent / fonts), `batch_design` `U` for scale and weight changes, `get_screenshot` for the AI slop test.

- [ ] **Step 1: Draft bolder.md against the section structure above**
- [ ] **Step 2: Verify the authorial discipline checklist**
- [ ] **Step 3: Commit**

```bash
git add skills/pencil-design/references/bolder.md
git commit -m "feat(skill): add bolder reference for amplifying safe designs"
```

---

### Task 3: Author quieter.md

**Files:**
- Create: `skills/pencil-design/references/quieter.md`

**Section structure:**
1. Opening framing: quieter design is harder than bolder; subtlety needs precision. Reduce visual intensity in designs that are too loud, aggressive, or overstimulating, without losing personality and without going generic. Quieter is not grayscale; it's refined.
2. Register split: brand quieter = restrained palette, more whitespace, typographic air, drama reduced not eliminated, POV intact; product quieter = fewer accents, flatter cards, less colour, less motion; the tool disappears into the task.
3. Assess current state: identify intensity sources (saturation, contrast extremes, competing visual weight, animation excess, complexity, scale uniformity). `get_screenshot` and check for cognitive load (cross-link [cognitive-load.md](cognitive-load.md)).
4. Plan: pick the colour approach (desaturate vs restrict), the hierarchy approach (which elements stay bold, which recede), the simplification approach (what to remove entirely), and the sophistication signal (how to read as restrained without reading as boring).
5. Apply across dimensions:
   - Colour: reduce saturation (shift to 70–85%); soften palette; let neutrals do more work (10% accent rule from color-and-contrast.md); use tinted greys instead of pure greys; never gray-on-color (use a darker shade of the colour or transparency).
   - Weight: reduce font weights (900 → 600, 700 → 500); use weight, size, and space for hierarchy instead of colour and boldness; increase whitespace; reduce or remove borders.
   - Simplification: remove gradients, shadows, patterns, textures that don't serve purpose; simplify shapes; flatten visual hierarchy where possible; clean up blur effects and multiple shadows.
   - Motion: reduce animation distances (10–20px instead of 40px); gentler easing; remove decorative animations entirely; subtle micro-interactions; refined ease-out-quart; never bounce or elastic.
   - Composition: reduce scale jumps; align rogue elements back to grid; even out spacing rhythm.
6. NEVER list: never make everything the same size or weight (hierarchy still matters); never strip all colour (quiet ≠ grayscale); never eliminate personality (character through refinement, not absence); never sacrifice usability for aesthetics; never make everything small and light (some anchors needed); never use gray text on a coloured background.
7. Verify quality: still functional (tasks complete easily); still distinctive (character intact, not generic); better reading (text reads for longer); restrained, not absent (the POV survives the cuts).
8. Handoff to [polish.md](polish.md).

**Cross-links:** `[color-and-contrast.md](color-and-contrast.md)`, `[motion-design.md](motion-design.md)`, `[cognitive-load.md](cognitive-load.md)`, `[brand.md](brand.md)`, `[product.md](product.md)`.

**Pencil ops referenced:** `set_variables` (palette desaturation, motion-token reduction), `replace_all_matching_properties` (bulk weight reduction), `get_screenshot`.

- [ ] **Step 1: Draft quieter.md against the section structure above**
- [ ] **Step 2: Verify the authorial discipline checklist**
- [ ] **Step 3: Commit**

```bash
git add skills/pencil-design/references/quieter.md
git commit -m "feat(skill): add quieter reference for refining loud designs"
```

---

### Task 4: Author distill.md

**Files:**
- Create: `skills/pencil-design/references/distill.md`

**Section structure:**
1. Opening framing: distill = strip to essentials. Great design is simple, powerful, clean. Distill removes unnecessary complexity without removing meaning. Different from quieter (quieter reduces intensity; distill reduces *content*).
2. Register split: brand distill = the page makes one argument; everything supporting that argument stays, everything else cuts; product distill = each surface does one job; the job is named and obvious within three seconds.
3. Assess current state: identify what each surface is for (one sentence). `get_screenshot`. List every element on the surface and rate it: essential / supportive / decorative / inherited. Decorative and most inherited cut.
4. Plan: name the single purpose of the surface; choose what stays and what goes; decide whether the cuts produce a *quieter* result (cross-link to [quieter.md](quieter.md)) or a *bolder* one (more impact per remaining element).
5. Apply across dimensions:
   - Content: cut decorative sub-headings; cut redundant CTAs; cut metadata the user doesn't act on; cut sections that exist because *"a homepage usually has one"*.
   - Components: collapse three similar cards into one repeated; remove icon-text label pairs where the label is enough; remove dividers that the spacing already provides.
   - Hierarchy: with fewer elements, hierarchy tightens; promote the one remaining hero; demote everything else into supporting rhythm.
   - Surface treatment: with less content, the same surface can lose some chrome (card borders, shadows). Cross-link [color-and-contrast.md](color-and-contrast.md) for tinted-neutrals as a chrome substitute.
6. NEVER list: never distill the brief away (the surface still has to do its job); never distill personality away (signature moments earn their place — cross-link [delight.md](delight.md)); never confuse distill with strip-mall minimalism (less but better, not less and less); never remove content that's needed for accessibility (skip links, error messages, ARIA labels); never confuse distill with quieter (different work).
7. Verify quality: the surface's one job is more obvious than before; nothing supports decoration alone; the remaining elements have more presence per element; the user knows where to look first.
8. Handoff to [polish.md](polish.md).

**Cross-links:** `[quieter.md](quieter.md)`, `[delight.md](delight.md)`, `[cognitive-load.md](cognitive-load.md)`, `[brand.md](brand.md)`, `[product.md](product.md)`.

**Pencil ops referenced:** `batch_design` (delete-ops via `D` and re-layout via `U`), `get_screenshot` before-and-after, `find_empty_space_on_canvas` for the cut frames.

- [ ] **Step 1: Draft distill.md against the section structure above**
- [ ] **Step 2: Verify the authorial discipline checklist**
- [ ] **Step 3: Commit**

```bash
git add skills/pencil-design/references/distill.md
git commit -m "feat(skill): add distill reference for stripping to essentials"
```

---

### Task 5: Author harden.md

**Files:**
- Create: `skills/pencil-design/references/harden.md`

**Section structure:**
1. Opening framing: harden = production-readiness. The happy path is done; this pass adds resilience. Edge cases, error states, i18n, text overflow, long content, partial-failure modes. Skipping this pass is the single biggest gap in AI-generated design.
2. Register split: brand harden = how the page survives at 320px width, when images fail to load, when the user has reduced-motion or high-contrast set; product harden = the full state matrix per component (loading, error, empty, partial-failure, offline) and screen-level fault states (404, 500, 503, offline).
3. Assess current state: for each interactive node, list which states ship today (cross-link [states.md](states.md)). For each surface, list which screen-level fault states apply (404 / 500 / offline / partial-failure). For each text block, simulate 2x length and 0.5x length. For each image, simulate missing.
4. Plan: prioritise the gaps (state matrix > fault screens > overflow > i18n > prefers-* media queries); decide how many states ship now vs deferred-with-justification.
5. Apply across dimensions:
   - Component states: build hover, focus, pressed, disabled, loading, error states as siblings inside the `reusable` component (see [states.md](states.md) and [interaction-design.md](interaction-design.md)). Use `state` theme axis or sibling frames.
   - Screen-level fault states: build 404, 500, 503, offline, empty-state, no-permission frames (see [states.md](states.md) § Screen-level fault states).
   - Overflow: every text block tested at 2x length (line-clamp where applicable; flowing prose elsewhere); every container tested at varying content; every layout tested at 320px width.
   - i18n: replace dummy text with realistic German or Finnish (long words); flip RTL for one screenshot (cross-link [accessibility.md](accessibility.md)).
   - Prefers-* media queries: prefers-reduced-motion (cross-link [motion-design.md](motion-design.md)); prefers-contrast (verify contrast still passes); prefers-reduced-transparency (no glassmorphism shortcuts).
   - Error messages: every error states what went wrong, why, and how to fix (cross-link [ux-writing.md](ux-writing.md)).
6. NEVER list: never declare done with default-state-only on interactive components; never skip the 404 / 500 / offline trio on a product surface; never use Lorem Ipsum or single-character padding to fake content length; never claim accessibility without checking keyboard nav and focus order; never assume the user's network is fast or available; never use text-truncation as a substitute for thoughtful overflow handling.
7. Verify quality: state matrix complete per [states.md](states.md); fault states present; 320px and 1920px both render; long-content and missing-content cases handled; error copy meets the what/why/how-to-fix bar.
8. Handoff to [polish.md](polish.md).

**Cross-links:** `[states.md](states.md)`, `[flows.md](flows.md)`, `[interaction-design.md](interaction-design.md)`, `[accessibility.md](accessibility.md)`, `[ux-writing.md](ux-writing.md)`, `[motion-design.md](motion-design.md)`.

**Pencil ops referenced:** `batch_design` (state-sibling frames), `set_variables` (state-axis declaration on a `reusable`), `get_screenshot` for each new state.

- [ ] **Step 1: Draft harden.md against the section structure above**
- [ ] **Step 2: Verify the authorial discipline checklist**
- [ ] **Step 3: Commit**

```bash
git add skills/pencil-design/references/harden.md
git commit -m "feat(skill): add harden reference for production-readiness pass"
```

---

### Task 6: Author clarify.md

**Files:**
- Create: `skills/pencil-design/references/clarify.md`

**Section structure:**
1. Opening framing: clarify = the UX-copy pass. Labels, error messages, button text, empty-state copy, microcopy, instructions. Bad copy reads as machine-generated faster than bad colour. Different from distill (clarify rewrites; distill removes).
2. Register split: brand clarify = voice is part of the brand expression, warmer and more opinionated copy allowed; product clarify = neutral, outcome-named, specific. Both registers refuse the AI cliché list (see [ux-writing.md](ux-writing.md)).
3. Assess current state: list every piece of copy on the surface (labels, buttons, errors, captions, headings, body, empty states). Rate each: specific / generic / cliché. Generic and cliché both rewrite.
4. Plan: pick which copy gets character (warmer, more specific) and which stays neutral (form labels, button text on dangerous actions). Brand surfaces lean character; product surfaces lean neutral.
5. Apply across categories:
   - Button labels: outcome-named (*"Send invoice"* not *"Submit"*); never generic (*"OK"*, *"Continue"*, *"Done"* on critical actions).
   - Error messages: state what went wrong + why + how to fix. *"Invoice 4521 didn't send: Stripe rejected the card. Try a different payment method."* Not *"An error occurred"*.
   - Empty states: specific, warm, with a forward path (see [delight.md](delight.md) and [ux-writing.md](ux-writing.md)).
   - Form labels: noun-named, no colons, no asterisks (use *"Required"* helper text instead).
   - Microcopy on inputs: real placeholder examples, not *"e.g. john@example.com"*.
   - Headings: specific, never *"Welcome"* / *"Overview"* / *"Dashboard"* unless the user can't be more specific.
   - AI cliché list: strike *"Elevate"*, *"Seamless"*, *"Unleash"*, *"Next-Gen"*, *"Revolutionize"*, *"Empower"*, *"Unlock"*, *"Transform"*. Full list in [ux-writing.md](ux-writing.md).
6. NEVER list: never use Lorem Ipsum (writes obscure the absence of thought); never use *"Submit"* on a button that does something specific; never describe a destructive action with neutral language (*"Delete"* not *"Continue"*); never use a heading the user can't act on; never write copy that would survive being copy-pasted into a different product unchanged.
7. Verify quality: every button names its outcome; every error includes what/why/how-to-fix; no AI clichés remain; empty states have a forward path; the copy reads like a specific person wrote it, not a model.
8. Handoff to [polish.md](polish.md).

**Cross-links:** `[ux-writing.md](ux-writing.md)`, `[states.md](states.md)`, `[delight.md](delight.md)`, `[brand.md](brand.md)`, `[product.md](product.md)`.

**Pencil ops referenced:** `batch_design` `U` ops for text-node content updates, `search_all_unique_properties` to find every text node, `get_screenshot` for the after.

- [ ] **Step 1: Draft clarify.md against the section structure above**
- [ ] **Step 2: Verify the authorial discipline checklist**
- [ ] **Step 3: Commit**

```bash
git add skills/pencil-design/references/clarify.md
git commit -m "feat(skill): add clarify reference for UX-copy refinement"
```

---

### Task 7: Author adapt.md

**Files:**
- Create: `skills/pencil-design/references/adapt.md`

**Section structure:**
1. Opening framing: adapt = the cross-device, cross-context, cross-mode pass. Desktop → mobile, light → dark, default → high-contrast, English → German. The design holds together across the variation.
2. Register split: brand adapt = the page makes the same argument at 320px, 768px, and 1920px; the hero scales, the rhythm holds; product adapt = the surface does the same job on phone, tablet, and desktop; the chrome changes, the job stays consistent.
3. Assess current state: which breakpoints exist today (mobile / tablet / desktop / wide)? Which theme axes are declared (mode? state? density?)? `get_variables` to see the full token surface. `get_screenshot` at each breakpoint and theme.
4. Plan: identify which surfaces collapse to mobile naturally (single-column long-form) and which need redesign (sidebar + main, dashboard grids). Decide whether mobile is a redesign or a reflow.
5. Apply across dimensions:
   - Breakpoint behaviour: 320 / 768 / 1280 / 1920 as the standard four (cross-link [layout.md](layout.md)). Mobile-first sizing on `set_variables`. Single-column reflow as default; multi-column only if the content benefits.
   - Touch targets: 44x44px minimum on mobile (apply via padding or pseudo-element trick — cross-link forthcoming spatial-design enrichment in [layout.md](layout.md)).
   - Type scale: fluid scale on mobile (drop the top end of the modular scale); never use desktop hero sizes on mobile.
   - Mode adaptation: every colour variable has light + dark from declaration ([color-and-contrast.md](color-and-contrast.md)); test both modes per surface.
   - Density adaptation: declare a `density` theme axis if the product has compact / comfortable / spacious modes; reference tokens per density.
   - i18n: the layout absorbs 2x text length (German); RTL flip is clean (cross-link [accessibility.md](accessibility.md)).
   - Prefers-* adaptation: prefers-reduced-motion replaces expressive durations with zero ([motion-design.md](motion-design.md)); prefers-contrast bumps borders and text contrast.
6. NEVER list: never use desktop typography sizes on mobile (hero scales need to drop); never declare a `mode` theme without testing both; never declare a design responsive without screenshotting 320 and 1920; never use hover-only affordances on mobile (touch has no hover); never ship a design with a `display: none` mobile state (the content is needed somewhere); never confuse adapt with redesign (adapt is one design rendered across conditions; redesign is multiple designs).
7. Verify quality: screenshots at 320, 768, 1280, 1920 all hold the design's intent; light and dark both pass contrast; touch targets meet 44px on mobile; RTL renders cleanly; prefers-reduced-motion produces a sensible static version.
8. Handoff to [polish.md](polish.md).

**Cross-links:** `[layout.md](layout.md)`, `[color-and-contrast.md](color-and-contrast.md)`, `[motion-design.md](motion-design.md)`, `[accessibility.md](accessibility.md)`, `[modern-patterns.md](modern-patterns.md)`.

**Pencil ops referenced:** `set_variables` (theme axes, breakpoint tokens, density tokens), `U(frameId, { theme: { mode: "dark" } })` for mode-specific frames, `get_screenshot` at each breakpoint.

- [ ] **Step 1: Draft adapt.md against the section structure above**
- [ ] **Step 2: Verify the authorial discipline checklist**
- [ ] **Step 3: Commit**

```bash
git add skills/pencil-design/references/adapt.md
git commit -m "feat(skill): add adapt reference for cross-device variation"
```

---

### Task 8: Author optimize.md

**Files:**
- Create: `skills/pencil-design/references/optimize.md`

**Section structure:**
1. Opening framing: optimize = the performance and rendering pass. Most of this happens after handoff (engineering owns runtime perf), but the design carries decisions that determine the ceiling. Image weight, asset count, font-loading strategy, motion budget, render-blocking choices. Optimize is about the decisions the designer makes that engineering can't undo.
2. Register split: brand optimize = the hero image is sized for the device; the font subset matches what's on the page; the motion runs at 60fps on a phone; product optimize = the surface renders fast at first paint; skeletons replace spinners; perceived performance beats actual performance.
3. Assess current state: list every image, every font, every motion sequence, every shadow / blur effect on the surface. Estimate weight. Identify which contribute to first-paint vs which lazy-load.
4. Plan: pick the perceived-performance lane (skeleton-first / optimistic-UI / progressive-disclosure) and the actual-performance constraints (image weight ceiling, font-family count cap, motion-budget cap).
5. Apply across dimensions:
   - Images: declare image variants for different breakpoints; use `G(nodeId, "ai", "<prompt>")` for generated images that match the surface; document expected weights in `context` strings for engineering hand-off.
   - Fonts: two families maximum (display + body); optional third (mono). One weight per family for first paint; defer extras. Document the subset (Latin / extended / OpenType features) in `context`.
   - Motion budget: cap concurrent animations at three on any surface; declare `prefers-reduced-motion` fallbacks ([motion-design.md](motion-design.md)).
   - Skeleton states: every loaded content frame has a skeleton-state sibling that matches the line-height and shape of the loaded content. Skeletons go in before the design is *done* ([states.md](states.md)).
   - Optimistic UI: for actions that succeed >95% of the time, the success state appears immediately; failure is the exception ([flows.md](flows.md)).
   - Shadow / blur budget: blurs and large soft shadows cost render time on mobile. Cap layered shadows at two per element; cap surfaces with backdrop-blur to under five at a time.
6. NEVER list: never ship a design without skeleton states on slow surfaces; never use three or more font families (cap is two, plus one mono); never ship glassmorphism (it's expensive and AI slop); never stack five backdrop-blur surfaces on top of each other (perf collapses on mobile); never animate everything; never document image weights in design copy that engineering can't read.
7. Verify quality: skeleton states present; font-family count ≤ 2 (+ mono); motion budget under three concurrent; image variants declared per breakpoint; `prefers-reduced-motion` fallback present.
8. Handoff to [polish.md](polish.md).

**Cross-links:** `[motion-design.md](motion-design.md)`, `[states.md](states.md)`, `[flows.md](flows.md)`, `[modern-patterns.md](modern-patterns.md)`.

**Pencil ops referenced:** `set_variables` (font and motion tokens), `batch_design` (skeleton-state siblings, image-variant declarations), `context` strings for engineering hand-off.

- [ ] **Step 1: Draft optimize.md against the section structure above**
- [ ] **Step 2: Verify the authorial discipline checklist**
- [ ] **Step 3: Commit**

```bash
git add skills/pencil-design/references/optimize.md
git commit -m "feat(skill): add optimize reference for performance and rendering"
```

---

### Task 9: Enrich layout.md

**Files:**
- Modify: `skills/pencil-design/references/layout.md`

**What to add:**

1. **Hierarchy through multiple dimensions** — new section after the squint test. The table impeccable's spatial-design has, adapted:

   | Tool | Strong Hierarchy | Weak Hierarchy |
   |------|------------------|----------------|
   | Size | 3:1 ratio or more | <2:1 ratio |
   | Weight | Bold vs Regular | Medium vs Regular |
   | Colour | High contrast | Similar tones |
   | Position | Top / left (primary) | Bottom / right |
   | Space | Surrounded by whitespace | Crowded |

   With the rule: combine 2–3 dimensions at once. A heading that's larger, bolder, AND has more space above it.

2. **Cards are not required** — new section after layout patterns. Cards are overused. Spacing and alignment create grouping naturally. Use cards only when (a) content is distinct and actionable, (b) items need visual comparison in a grid, (c) content needs clear interaction boundaries. Never nest cards inside cards.

3. **Touch targets vs visual size** — new section toward the end. Buttons can look small but need 44x44px minimum touch targets. Apply via padding or sibling frame extending the touchable area:

   ```
   U("<iconButton>", { width: 24, height: 24 })
   T1=I("iconButton", { type: "frame", x: -10, y: -10, width: 44, height: 44, fill: "transparent", role: "button" })
   ```

4. **Optical adjustments** — new section. Text at the container edge looks indented due to letterform whitespace; use negative margin (-0.05em equivalent in Pencil) for optical alignment. Geometrically centred icons often look off-centre; play icons shift right, arrows shift toward their direction.

5. **Semantic spacing tokens** — short addition to the 4pt section. Name spacing tokens by relationship (`$spaceSm`, `$spaceLg`), not by value (`$spacing8`). Use `gap` (auto layout) for sibling spacing; eliminates margin-collapse hacks.

- [ ] **Step 1: Add the five sections above to layout.md at the indicated points**
- [ ] **Step 2: Verify the additions match the existing voice (italic-quoted examples, register-aware framing, no em dashes, AusE)**
- [ ] **Step 3: Commit**

```bash
git add skills/pencil-design/references/layout.md
git commit -m "feat(skill): enrich layout with hierarchy table, touch targets, optical adjustments"
```

---

### Task 10: Enrich typography.md

**Files:**
- Modify: `skills/pencil-design/references/typography.md`

**What to add:**

1. **Extreme weight pairing** — new sub-section under "Weight contrast over size contrast". Pairing 900 with 200 (or 300) reads as committed; pairing 600 with 400 reads as default. Reach for the extremes when the surface earns the drama. Most modern variable fonts (Geist, Inter, Söhne) support the full weight range; activate it.

2. **Monospace as intentional accent** — new sub-section under "Special moves". Monospace as a default body font reads as developer-tool reflex. Monospace as a deliberate accent (a data column, a code reference, a kicker label) signals intent. Pair mono with a grotesque body, not with another mono.

3. **Condensed and extended widths** — new sub-section under "Pairing rules". Modern variable fonts ship multiple widths. A condensed display + regular body, or a regular display + extended body, adds dimension without changing typeface families. Sparingly; one width contrast per surface, not three.

- [ ] **Step 1: Add the three sections above to typography.md at the indicated points**
- [ ] **Step 2: Verify the additions match the existing voice**
- [ ] **Step 3: Commit**

```bash
git add skills/pencil-design/references/typography.md
git commit -m "feat(skill): enrich typography with extreme weight, mono-as-accent, width variation"
```

---

### Task 11: Enrich color-and-contrast.md

**Files:**
- Modify: `skills/pencil-design/references/color-and-contrast.md`

**What to add:**

1. **Never gray on color** — new sub-section under "Tinted neutrals". If the design has gray text on a coloured background, replace the gray with a darker (or lighter) shade of the *same* hue, or use transparency on the text colour. Gray-on-colour reads as accidental; same-hue text reads as system.

2. **Dominant colour strategy (60% rule)** — new sub-section under "The four palette strategies", specifically as a refinement of the *Committed* strategy. When one colour drives the design, let it own 60% of the visible surface area (not 30%, not 80%). The remaining 40% is neutrals plus a single accent or contrasting role. The 60% commitment is what reads as confident.

3. **Gentler contrasts where it doesn't matter** — new sub-section under "Common dark-mode failures" (or as its own section). High-contrast everywhere creates noise. Reserve high contrast for the focal points; let secondary elements use gentler contrast (3:1 to 4:1). The squint test reveals whether contrast is doing hierarchy work or competing.

- [ ] **Step 1: Add the three sections above to color-and-contrast.md at the indicated points**
- [ ] **Step 2: Verify the additions match the existing voice**
- [ ] **Step 3: Commit**

```bash
git add skills/pencil-design/references/color-and-contrast.md
git commit -m "feat(skill): enrich color with never-gray-on-color, 60% rule, gentler-contrast"
```

---

### Task 12: Enrich motion-design.md

**Files:**
- Modify: `skills/pencil-design/references/motion-design.md`

**What to add:**

1. **Scroll-anchored reveal staggering** — new sub-section under "Brand motion". When a hero sequence reveals on scroll-into-view, each step gets 200–300ms with 50–100ms stagger between steps. Three to five steps is the ceiling; more than that reads as choreographed-for-its-own-sake. The reveal happens once per session; don't replay on scroll-back.

2. **Motion intensity reduction recipes** — new section near the end, for use with quieter.md. When toning motion down: cut translate distances by half (40px → 20px → 10px); shift easing toward ease-out-quart (less character than expo); reduce duration by 25–40%; remove decorative motion entirely (only keep functional). Document the original motion intent in `context` strings if engineering needs to know what was reduced from.

- [ ] **Step 1: Add the two sections above to motion-design.md at the indicated points**
- [ ] **Step 2: Verify the additions match the existing voice**
- [ ] **Step 3: Commit**

```bash
git add skills/pencil-design/references/motion-design.md
git commit -m "feat(skill): enrich motion with scroll-anchored staggering and reduction recipes"
```

---

### Task 13: Wire scaffold refs into SKILL.md

**Files:**
- Modify: `skills/pencil-design/SKILL.md` (situational routing region around lines 306–313, Reference index region around lines 414–432)

**What to add:**

1. **Situational routing** — add eight bullets in the appropriate region of SKILL.md (the *"User asks for X, load Y reference"* table):

   - **User asks to make a design *bolder*, more *impactful*, more *distinctive*, or *more confident*.** Load `references/bolder.md`. It owns the AI-slop refusal for *bolder* (no purple gradients, no glassmorphism, no neon-on-dark), and the dimension-by-dimension amplification recipes.
   - **User asks to make a design *quieter*, *calmer*, *less aggressive*, or *more restrained*.** Load `references/quieter.md`. It owns the desaturation, weight-reduction, and motion-quietening recipes, plus the *quiet ≠ generic* discipline.
   - **User asks to *distill*, *simplify*, *strip back*, or *remove what doesn't earn its place*.** Load `references/distill.md`. It owns the essential / supportive / decorative / inherited rating, and the cut-vs-promote framework.
   - **User asks to *harden*, prepare for production, add error / loading / empty / edge-case states, or asks about i18n and overflow.** Load `references/harden.md`. It owns the state-matrix completeness checklist, the screen-level fault states, and the prefers-* media queries.
   - **User asks to *clarify*, fix the UX copy, rewrite labels / errors / microcopy, or asks about button text and form labels.** Load `references/clarify.md` plus `references/ux-writing.md`. Clarify is the *which copy to rewrite* pass; ux-writing.md is the *how to rewrite* depth.
   - **User asks to *adapt* the design to mobile, tablet, dark mode, high-contrast, RTL, or other contexts.** Load `references/adapt.md`. It owns breakpoints, theme-axis discipline, touch-targets, i18n, and prefers-* adaptation.
   - **User asks to *optimize* for performance, reduce asset weight, add skeleton states, or improve perceived speed.** Load `references/optimize.md`. It owns the font-cap, motion budget, skeleton-state, and optimistic-UI guidance.
   - **User asks for a *polish* pass, final-pass alignment, or *cleanup before shipping*.** Load `references/polish.md`. It owns the alignment / token-consistency / detail-coherence trio and the both-modes verification.

2. **Reference index** — append eight entries to the bottom-of-SKILL.md Reference index. Each one-line entry describing what the file owns and when to load. Pattern matches existing entries (e.g. line 432 for delight.md).

3. **Update delight.md routing** (line 311) so that *"adding personality vs final polish"* is unambiguous: delight = personality; polish = alignment-and-consistency.

- [ ] **Step 1: Add the eight situational routing bullets in the appropriate region of SKILL.md**
- [ ] **Step 2: Append eight Reference index entries**
- [ ] **Step 3: Update the delight.md routing line to disambiguate from polish.md**
- [ ] **Step 4: Verify routing reads cleanly with the new entries (no duplicates, no contradictions)**
- [ ] **Step 5: Commit**

```bash
git add skills/pencil-design/SKILL.md
git commit -m "feat(skill): wire scaffold refs into SKILL.md routing and reference index"
```

---

## Out of scope

- **Build / packaging changes.** Impeccable's 11-platform build system, `marketplace.json`, and provider-config pattern are noted in `[[reference_impeccable]]` but explicitly deferred; this plan only touches the SKILL content.
- **Sub-command splitting.** Adding `/pencil-design bolder` style slash-commands is a different architectural call; this plan keeps the monolithic-skill structure.
- **Evals.** New reference files don't get standalone evals in this plan; existing skill evals continue to cover the SKILL.md workflow. A follow-up plan may add per-scaffold-ref evals.
- **CHANGELOG.md update.** Hold per `[[feedback_no_version_bumps]]`; changes go in `[Unreleased]` only when Travis confirms scope.

---

## Self-review

**Spec coverage check:**
- Eight scaffold refs requested → eight tasks (1–8). ✓
- Enrich four topic refs in-place → four tasks (9–12). ✓
- Handoff-to-polish pattern → polish.md authored first (Task 1); every other scaffold ref ends with a polish handoff per the discipline rule. ✓
- Pencil-flavoured, not impeccable-cloned → discipline rule requires MCP-op references per file; per-task sections name the ops. ✓

**Placeholder check:** No TBD / TODO / "fill in details" remains. Each task's section structure names what goes in each section.

**Type consistency:** Cross-references between scaffold refs are mutual (quieter ↔ distill, harden ↔ states, etc.); polish.md is the universal handoff target named consistently across tasks 2–8.

**Voice consistency:** Authorial discipline section at the top applies uniformly; each task's verification step references it.

---

## Execution handoff

Plan complete and saved to `docs/superpowers/plans/2026-05-16-impeccable-style-references.md`.

Per `[[feedback_no_parallel_agents]]`, subagent-driven execution is ruled out. Inline execution via `superpowers:executing-plans`, working through tasks 1–13 sequentially. Commit between tasks per the plan; user can review each file as it lands.
